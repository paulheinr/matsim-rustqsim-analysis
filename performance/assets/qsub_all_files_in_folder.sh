#!/bin/bash
for entry in "$1"/*
do
  qsub "$entry"
done