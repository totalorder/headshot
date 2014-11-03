package main

import "fmt"

import (
	_ "github.com/lib/pq"
	"database/sql"
	"log"
	"time"
	"net/http"
	"io/ioutil"
	"sync"
	"os/exec"
	"math"
	"strings"
)

const (
	OK = "OK"
	WARN = "Warn"
	FAILED = "Failed"
	INVALID = "Invalid"
)

type Status struct {
	code string
	short_desc string
	desc string
	monitor_id string
	timestamp time.Time
}

func (s *Status) save(db *sql.DB) error {
	fmt.Printf("Saving status: {monitor_id: %s, code: %s, short_desc: %s, desc: %s, timestamp: %s}\n", s.monitor_id, s.code, s.short_desc, s.desc, s.timestamp)
	rows, err := db.Query(`INSERT INTO monitor_status (monitor_id, code, short_desc, "desc", timestamp)
										 		 VALUES ($1, 		 $2,   $3, 		   $4, 	 $5)`,
		s.monitor_id, s.code, s.short_desc, s.desc, s.timestamp)
    defer rows.Close()
	return err
}

type Monitor interface {
	work(db *sql.DB)
	getId() string
	getInterval() time.Duration
}

type BaseMonitor struct {
	id string
	interval time.Duration
}

func (b BaseMonitor) getId() string {
	return b.id
}

func (b BaseMonitor) getInterval() time.Duration {
	return b.interval
}

func (b BaseMonitor) work(db *sql.DB) {
	fmt.Println("Not implemented!")
}

func runMonitor(m Monitor, db *sql.DB) {
	for {
		m.work(db)
		time.Sleep(m.getInterval())
	}
}

type URLMonitor struct {
	BaseMonitor
	url string
	warn_latency time.Duration
}

func (u URLMonitor) work(db *sql.DB) {
	var status Status
	status.monitor_id = u.id
	status.timestamp = time.Now()
	start_time := time.Now()
	resp, err := http.Get("http://example.com/")
	if err != nil {
		status.code = FAILED
		status.short_desc = resp.Status
		status.save(db)
		return
	}

	defer resp.Body.Close()
	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		status.code = FAILED
		status.short_desc = fmt.Sprintf("Could not read body (%s) %s", resp.Status, err)[:128]
		status.desc = fmt.Sprintf("Could not read body (%s) %s", resp.Status, err)
		status.save(db)
		return
	}

	latency := time.Now().Sub(start_time)
	if (latency >= u.warn_latency) {
		status.code = WARN
		status.short_desc = fmt.Sprintf("(200) Latency is %d ms", latency / time.Millisecond)
		status.save(db)
	} else {
		status.code = OK
		status.short_desc = "(200) OK"
		status.save(db)
	}
}

type LocalProcessMonitor struct {
	BaseMonitor
	command string
	success_message string
}

func (u LocalProcessMonitor) work(db *sql.DB) {
	var status Status
	status.monitor_id = u.id
	status.timestamp = time.Now()
	split_command := strings.Split(u.command, " ")
	out_bytes, err := exec.Command(split_command[0], split_command[1:]...).CombinedOutput()
	out := string(out_bytes[:])

	if err != nil {
		desc := err.Error() + out
		status.code = FAILED
		status.short_desc = desc[:int(math.Min(float64(len(desc)),128))]
		status.desc = desc
		status.save(db)
		return
	}

	short_desc := u.success_message + out
	status.code = OK
	status.short_desc = short_desc[:int(math.Min(float64(len(short_desc)),128))]
	status.desc = out
	status.save(db)
}

func createURLMonitors(monitors []Monitor, db *sql.DB) []Monitor {
	rows, err := db.Query(`SELECT m.id, m.interval, u.url, u.warn_latency
						   FROM monitor_monitor AS m
						   JOIN monitor_urlmonitor as u ON (m.id = u.monitor_ptr_id)`)
	if err != nil {
		log.Panic(err)
	}
	defer rows.Close()

	for rows.Next() {
		var urlmonitor URLMonitor
		var interval int64
		var warn_latency int64
		if err := rows.Scan(&urlmonitor.id, &interval, &urlmonitor.url, &warn_latency); err != nil {
			log.Panic(err)
		}
		urlmonitor.interval = time.Duration(interval) * time.Second
		urlmonitor.warn_latency = time.Duration(warn_latency) * time.Millisecond
		fmt.Print(urlmonitor.warn_latency)
		monitors = append(monitors, urlmonitor)
	}
	return monitors
}

func createLocalProcessMonitors(monitors []Monitor, db *sql.DB) []Monitor {
	rows, err := db.Query(`SELECT m.id, m.interval, u.command, u.success_message
						   FROM monitor_monitor AS m
						   JOIN monitor_localprocessmonitor as u ON (m.id = u.monitor_ptr_id)`)
	if err != nil {
		log.Panic(err)
	}
	defer rows.Close()

	for rows.Next() {
		var lpmonitor LocalProcessMonitor
		var interval int64
		if err := rows.Scan(&lpmonitor.id, &interval, &lpmonitor.command, &lpmonitor.success_message); err != nil {
			log.Panic(err)
		}
		lpmonitor.interval = time.Duration(interval) * time.Second
		monitors = append(monitors, lpmonitor)
	}
	return monitors
}

func createMonitors(db *sql.DB) []Monitor {
	var monitors []Monitor
	monitors = createURLMonitors(monitors, db)
	monitors = createLocalProcessMonitors(monitors, db)
	return monitors
}

func main() {
	db, err := sql.Open("postgres", "user=headshot dbname=headshot password=headshot")
	if err != nil {
		log.Panic(err)
	}
	defer db.Close()

	monitors := createMonitors(db)

	var wg sync.WaitGroup
	for _, monitor := range monitors {
		fmt.Printf("Starting monitor %s...\n", monitor.getId())
		wg.Add(1)
		go runMonitor(monitor, db)
	}

	fmt.Println("Monitors are running...")
	wg.Wait()
	fmt.Println("All monitors are have exited. Shutting down...")
}
