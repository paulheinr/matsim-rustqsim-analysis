#!/bin/bash
for entry in "$1"/*
do
  sbatch "$entry"
done