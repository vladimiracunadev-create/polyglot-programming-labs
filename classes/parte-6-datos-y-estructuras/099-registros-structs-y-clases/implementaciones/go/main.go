package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Persona struct {
	Nombre string
	Edad   int
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	edad, _ := strconv.Atoi(t[1])
	p := Persona{Nombre: t[0], Edad: edad}
	fmt.Printf("Persona(nombre=%s, edad=%d)\n", p.Nombre, p.Edad)
}
