package main

import (
	"os"
	"path/filepath"
	"strings"
)

func explorer(initialDir string) []string {
	ext := ""
	files := make([]string, 0)
	filepath.Walk(initialDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		ext = filepath.Ext(path)
		if ext == ".pdf" {
			files = append(files, path)
		}
		return nil

	})
	return files
}

func renameFile(file string) error {
	newFile := file + ".rango"
	err := os.Rename(file, newFile)
	if err != nil {
		return err
	}
	return nil
}

func restoreFile(file string) error {
	newFile := strings.Split(file, ".rango")[0]
	err := os.Rename(file, newFile)
	if err != nil {
		return err
	}
	return nil
}
