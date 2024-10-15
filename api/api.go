package main

import (
	"fmt"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func main() {
	InitDB()

	r := chi.NewRouter()

	r.Use(middleware.Logger)
	r.Get("/", apiPage)

	fmt.Println("Server is running on http://localhost:3000")
	http.ListenAndServe(":3000", r)
}
