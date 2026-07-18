package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	linea, _ := reader.ReadString('\n')
	campos := strings.Fields(linea)

	// Go: tipado estático explícito; conversión float64(cantidad) obligatoria.
	precioUnitario, _ := strconv.ParseFloat(campos[0], 64)
	cantidad, _ := strconv.Atoi(campos[1])
	descuento, _ := strconv.ParseFloat(campos[2], 64)

	subtotal := precioUnitario * float64(cantidad)
	total := subtotal * (1 - descuento)

	fmt.Printf("Total: %.2f\n", total)
}
