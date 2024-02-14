package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

type Position struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
}

type Player struct {
	Position Position `json:"position"`
	Health   int      `json:"health"`
}

type NPC struct {
	Position Position `json:"position"`
	Type     string   `json:"type"`
}

type Game struct {
	ID     string `json:"game_id"`
	Player Player `json:"player"`
	NPCS   []NPC  `json:"npcs"`
}

type GameRepository struct {
	Games []Game `json:"games"`
}

var gameRepository GameRepository

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
}

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Home Page")
}

func reader(conn *websocket.Conn) {
	for {
		// Read message from browser
		msgType, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}

		// Unmarshal the JSON string into a Game object
		var game Game
		err = json.Unmarshal(msg, &game)
		if err != nil {
			log.Println(err)
			return
		}

		// Add the new game to the repository or update the existing game
		var found bool
		for i, g := range gameRepository.Games {
			if g.ID == game.ID {
				gameRepository.Games[i] = game
				found = true
				break
			}
		}
		if !found {
			gameRepository.Games = append(gameRepository.Games, game)
		}

		responseMessage := "Game updated"

		// Print the updated game repository in json format
		log.Println(gameRepository)

		// Write message back to the browser
		if err = conn.WriteMessage(msgType, []byte(responseMessage)); err != nil {
			log.Println(err)
			return
		}
	}
}

func wsEndpoint(w http.ResponseWriter, r *http.Request) {
	// Upgrade this connection to a WebSocket
	// connection
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
	}

	log.Println("Client Connected !")

	// Send a message to the newly connected WebSocket
	ws.WriteMessage(1, []byte("Hi Client"))

	reader(ws)
}

func setupRoutes() {
	http.HandleFunc("/", homePage)
	http.HandleFunc("/ws", wsEndpoint)
}

func main() {
	fmt.Println("Go WebSockets")
	setupRoutes()
	log.Fatal(http.ListenAndServe(":8080", nil))
}
