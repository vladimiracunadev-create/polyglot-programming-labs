package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func dividir(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("division")
	}
	return a / b, nil
}

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	f := strings.Fields(line)
	a, _ := strconv.Atoi(f[0])
	b, _ := strconv.Atoi(f[1])
	res, err := dividir(a, b)
	if err != nil {
		fmt.Printf("err=%s\n", err)
	} else {
		fmt.Printf("ok=%d\n", res)
	}
}
