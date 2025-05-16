#!/bin/bash
for file in materials/*.py; do
  echo "Running $file"
  ./build/X86/gem5.opt "$file"
done
