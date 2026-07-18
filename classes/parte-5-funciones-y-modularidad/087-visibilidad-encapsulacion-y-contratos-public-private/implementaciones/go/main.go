package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// saldo en minúscula: privado del paquete.
type cuenta struct {
	saldo int64
}

func (c *cuenta) depositar(monto int64) {
	c.saldo += monto
}

func (c *cuenta) obtenerSaldo() int64 {
	return c.saldo
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	n, _ := strconv.ParseInt(strings.TrimSpace(line), 10, 64)
	c := &cuenta{}
	c.depositar(n)
	c.depositar(n)
	fmt.Printf("saldo=%d\n", c.obtenerSaldo())
}
