#!/bin/sh

# to avoid domaine resolving issues happening during update
echo 'nameserver 8.8.8.8' > /etc/resolv.conf

echo "-------- npm install --------"

npm install

echo "-------- npm update --------"

npm update --save

echo "-------- done --------"
