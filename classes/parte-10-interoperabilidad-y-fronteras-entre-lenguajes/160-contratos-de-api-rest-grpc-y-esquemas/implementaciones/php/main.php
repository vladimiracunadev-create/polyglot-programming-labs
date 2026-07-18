<?php
[$metodo, $recurso] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "contrato=$metodo /$recurso\n";
