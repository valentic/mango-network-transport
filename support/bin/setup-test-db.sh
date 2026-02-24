#!/bin/bash

##########################################################################
#
#   Setup the test database
#
#   During development, we use a test database to make sure we do not
#   interfer with the production database. This script creates and 
#   initializes the test database (mango-test).
#
#   It is designed to be run from the mango/support/bin directory
#   which contains the .conf files, update.py
#
#   Create the database with:
#
#       createdb mango-test
#
#   2026-02-20  Todd Valentic
#               Initial implmentation
#
##########################################################################

export MANGO_DATABASE_URI=postgresql://@/mango-test

. profile

./update.py status.conf
./update.py device.conf
./update.py instrument.conf
./update.py system_model.conf
./update.py station.conf
./update.py fusionproducts.conf
./update.py processed_products.conf
./update.py stationinstrument.conf
./update.py statisticproducts.conf

