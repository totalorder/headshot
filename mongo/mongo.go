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
	_, err := db.Query(`INSERT INTO monitor_status (monitor_id, code, short_desc, "desc", timestamp)
										 		 VALUES ($1, 		 $2,   $3, 		   $4, 	 $5)`,
		s.monitor_id, s.code, s.short_desc, s.desc, s.timestamp)
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
	fmt.Println("Loopiung")
	for {
		fmt.Println("Loopaabng")
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
	fmt.Println("Downloading url")
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

func main() {
	db, err := sql.Open("postgres", "user=headshot dbname=headshot password=headshot")
	if err != nil {
		log.Panic(err)
	}

	monitors := []Monitor{
		URLMonitor{BaseMonitor:BaseMonitor{
			id:"Localhost",
			interval: 10 * time.Second},
			url: "http://localhost:8000/",
			warn_latency: 200 * time.Millisecond}}

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
