package main

import "strings"
import "os"
import "bufio"
import "fmt"

func main() {
	reader := bufio.NewReader(os.Stdin)
	counter := make(map[string]int64)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		line = strings.TrimSpace(line)
		splits := strings.Split(line, " ")
		for i := range splits {
			w := splits[i]
			if w != "" {
				counter[w] += 1
			}
		}
	}
	for w := range counter {
		fmt.Println(w, "\t", counter[w])
	}
}
