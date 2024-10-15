package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
)

var db *sql.DB

func InitDB() {
	var err error
	connectionString := "postgres://wishYourPartnerUser:7437@localhost/wishyourpartner?sslmode=disable"
	db, err = sql.Open("postgres", connectionString)
	if err != nil {
		log.Fatal(err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Успешно подключено к базе данных!")
}

func CloseDB() {
	if db != nil {
		db.Close()
	}
}
