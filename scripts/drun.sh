#!/usr/bin/env bash
docker run --env-file ./Scraping/email.env -i  -p 4555:4555 ksula0155/servus:latest