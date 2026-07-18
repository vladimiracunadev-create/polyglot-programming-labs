package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	t := strings.Fields(line)
	nombre := t[0]
	edad, _ := strconv.Atoi(t[1])
	fmt.Printf("{\"nombre\": \"%s\", \"edad\": %d}\n", nombre, edad)
}
