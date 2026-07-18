<?php
[$clave, $valor] = preg_split('/\s+/', trim(fgets(STDIN)));
echo "serializado=$clave:$valor\n";
