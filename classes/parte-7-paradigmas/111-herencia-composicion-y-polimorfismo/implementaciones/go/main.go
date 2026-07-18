package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Animal interface {
	sonido() string
}

type Perro struct{}
type Gato struct{}
type Vaca struct{}

func (Perro) sonido() string { return "guau" }
func (Gato) sonido() string  { return "miau" }
func (Vaca) sonido() string  { return "muu" }

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	tipo := strings.TrimSpace(line)
	var a Animal
	switch tipo {
	case "perro":
		a = Perro{}
	case "gato":
		a = Gato{}
	default:
		a = Vaca{}
	}
	fmt.Printf("sonido=%s\n", a.sonido())
}
