package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"unicode"
)

func main() {
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	w := strings.TrimSpace(line)
	seguro := len(w) > 0
	for _, c := range w {
		if !unicode.IsLetter(c) && !unicode.IsDigit(c) {
			seguro = false
		}
	}
	res := "false"
	if seguro {
		res = "true"
	}
	fmt.Printf("seguro=%s\n", res)
}
