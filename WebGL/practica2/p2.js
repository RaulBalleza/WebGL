// Vertex shader program
var VSHADER_SOURCE =
  'attribute vec4 a_Position;\n' +
  'attribute vec4 a_Color;\n' +
  //'uniform mat4 u_MvpMatrix;\n' +
  'varying vec4 v_Color;\n' + // varying variable
  'void main() {\n' +
  '  gl_Position = a_Position;\n' +
  '  v_Color = a_Color;\n' +  // Pass the data to the fragment shader
  '}\n';


// Fragment shader program
var FSHADER_SOURCE =
  'precision mediump float;\n' +
  'varying vec4 v_Color;\n' + // Receive the data from the vertex shader
  'void main() {\n' +
  //'  gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n' +
  '  gl_FragColor = v_Color;\n' +
  '}\n';

//Array donde se guardan las posiciones de las figuras y sus numeros
var boardGame = [];

var coordFig = [];

var ctxTexto;

var fila = 0;
var columna = 0;
var swap = 0;

function main() {
    // Retrieve <canvas> element
    var canvas = document.getElementById('webgl');

    // TOMAR CONTEXTO DE LA CAPA CANVAS DE TEXTO
    var canvasTexto = document.getElementById('capa_texto');
    ctxTexto = canvasTexto.getContext('2d');

    // DIBUJAR ETIQUETAS DE TEXTO
    ctxTexto.font = "bold 35px verdana, sans-serif";
    ctxTexto.fillStyle = "#000";

    //Obtener la matriz random de como quedara el tablero
    getBoardGame();

    // Get the rendering context for WebGL
    var gl = getWebGLContext(canvas);
    if (!gl) {
        console.log('Failed to get the rendering context for WebGL');
        return;
    }

    // Initialize shaders
    if (!initShaders(gl, VSHADER_SOURCE, FSHADER_SOURCE)) {
        console.log('Failed to intialize shaders.');
        return;
    }

    // Get the storage location of a_Position
    var a_Position = gl.getAttribLocation(gl.program, 'a_Position');
    if (a_Position < 0) {
        console.log('Failed to get the storage location of a_Position');
        return;
    }

    // Specify the color for clearing <canvas>
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    canvasTexto.onmousedown = function (ev) {
        
        //drawBoard(gl);
        //drawLines(gl);
        //click(ev, gl, canvas, a_Position);
        //drawPoints(gl, g_points, a_Position);

        var x = ev.clientX; // x coordinate of a mouse pointer
        var y = ev.clientY; // y coordinate of a mouse pointer
        var rect = ev.target.getBoundingClientRect();
        
        if (rect.left <= x && x < rect.right && rect.top <= y && y < rect.bottom) {

            var x_in_canvas = x - rect.left;
            var y_in_canvas = rect.bottom - y;

            var coord = convertirCoordenadas(x_in_canvas, y_in_canvas, canvas);

            var x_realCoord = coord[0];
            var y_realCoord = coord[1];

            makeSwap(x_realCoord, y_realCoord);
            
        }

    };

    // Clear <canvas>
    gl.clear(gl.COLOR_BUFFER_BIT);
    
    ctxTexto.clearRect(0, 0, canvas.width, canvas.height);

    //Dibujar el tablero completo del juego
    drawBoard(gl);

    //Dibujar las lineas negras del tablero
    drawLines(gl);

}

function makeSwap(x, y) {
    //Recorrer cada fila y columna para ver cual es la que se seleccion
    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            if ((x >= -1.0+(i*0.5) && x <= -1.0+((i+1)*0.5)) && (y > 1.0-((j+1)*0.5)) && y < 1.0-(j*0.5)) {
                
                //Si se selcciona un cuadrado != al negro
                if (boardGame[j][i] != 16 && swap == 0) {
                    fila = j;
                    columna = i;
                    swap++;
                    document.getElementById('seleccion').innerHTML = "Pieza seleccionada: "+boardGame[j][i];
                //Si se selcciona un cuadrado != al negro y anteriormente igua
                } else if (boardGame[j][i] != 16 && swap == 1) {
                    fila = j;
                    columna = i;
                    document.getElementById('seleccion').innerHTML = "Pieza seleccionada: "+boardGame[j][i];
                //Si se selcciona el cuadrado negro y antes se selcciono uno !=
                } else if (boardGame[j][i] == 16 && swap == 1) {

                    //Valor del cuadro anterior
                    var aux = boardGame[fila][columna];
                    //Valor del cuadro negro
                    var aux2 = boardGame[j][i];

                    //Se intercambia posiciones en la matriz
                    boardGame[j][i] = aux;
                    boardGame[fila][columna] = aux2;
                    
                    swap = 0;
                    document.getElementById('seleccion').innerHTML = "Pieza seleccionada: ";

                    //Llamar de nuevo al main
                    main();

                }                
            }
        }
    }
}

function convertirCoordenadas(x,y,canvas){
    //Valor de la mitad de la pantalla en X y Y
	var puntoMedioX = canvas.width/2.0;
	var puntoMedioY = canvas.height/2.0;
    
    //De la mitad, se obtiene cuanto vale cada punto
	var valorX = puntoMedioX/1.0;
	var valorY = puntoMedioY/1.0;
    
    //Guardar el valor final de X y Y
	var valorFinalX = 0;
	var valorFinalY = 0;

	valorFinalX = ((puntoMedioX - x)/valorX)*-1
	valorFinalY = ((puntoMedioY - y)/valorY)*-1

	return [valorFinalX, valorFinalY]
}

function drawBoard(gl) {
    // Clear <canvas>
    gl.clear(gl.COLOR_BUFFER_BIT);

    var p1x = -1.0, p1y = 1.0;
    var p2x = -1.0, p2y = 0.5;
    var p3x = -0.5, p3y = 1.0;
    var p4x = -0.5, p4y = 0.5;
    var color = 0;
    var totalVertices = 0;

    //Coordenadas donde comienza el texto
    var xText = 60;
    var yText = 85;

    //Ciclos para colocar los cuadros de colores
    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            
            //Decidir el color (Par Verde, impar Rojo)
            //Rojo
            if (boardGame[i][j]%2 != 0){
                color = 0;
                //Verde
            } else if (boardGame[i][j]%2 == 0) {
                color = 1;
            }
            
            //Forzar a que se pinte negro cuando sea 16
            if (boardGame[i][j] == 16)  {
                color = 2;
            }
            
            //Añadir coordenada de cada punto de la figura y su color
            coordFig.push(p1x);
            coordFig.push(p1y);
            pushRGB(color);
            coordFig.push(p2x);
            coordFig.push(p2y);
            pushRGB(color);
            coordFig.push(p3x);
            coordFig.push(p3y);
            pushRGB(color);
            coordFig.push(p4x);
            coordFig.push(p4y);
            pushRGB(color);

            //Sumar 0.5 en X para dibujar el cuadro
            p1x += 0.5;
            p2x += 0.5;
            p3x += 0.5;
            p4x += 0.5;

            //suma el total de vertices
            totalVertices = 4;
            
            // Write the positions of vertices to a vertex shader
            var n = initVertexBuffers(gl, totalVertices);
            if (n < 0) {
                console.log('Failed to set the positions of the vertices');
                return;
            }
            
            // Draw the rectangle
            gl.drawArrays(gl.TRIANGLE_STRIP, 0, n);
            
            //Color texto de los numeros
            ctxTexto.fillText(boardGame[i][j],xText,yText);
            
            xText += 150
            
            coordFig = [];      
        
        }
        
        yText += 145;
        xText = 60;

        p1x = -1.0;
        p2x = -1.0;
        p3x = -0.5;
        p4x = -0.5;

        //Bajar 0.5 en el eje de las Y
        p1y -= 0.5;
        p2y -= 0.5;
        p3y -= 0.5;
        p4y -= 0.5;

    }
}

function drawLines(gl) {
    //Dibujar las lineas horizontales
    var y = 0.5;
    var x1 = -1.0;
    var x2 = 1.0;
    for (var i = 0; i < 3; i++) {
        var puntosLineas = [];
    
        puntosLineas.push(x1);
        puntosLineas.push(y);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);

        puntosLineas.push(x2);
        puntosLineas.push(y);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);

        y -= 0.5;

        // Write the positions of vertices to a vertex shader
        var n = initVertexBuffersLineas(gl, puntosLineas);
        if (n < 0) {
            console.log('Failed to set the positions of the vertices');
            return;
        }
        
        // Draw the lines
        gl.drawArrays(gl.LINES, 0, n);
    }

    //Dibujar las lineas verticales
    var x = -0.5;
    var y1 = 1.0;
    var y2 = -1.0;
    for (var i = 0; i < 3; i++) {
        var puntosLineas = [];

        puntosLineas.push(x);
        puntosLineas.push(y1);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);

        puntosLineas.push(x);
        puntosLineas.push(y2);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);
        puntosLineas.push(0.0);

        x += 0.5;        

        // Write the positions of vertices to a vertex shader
        var n = initVertexBuffersLineas(gl, puntosLineas);
        if (n < 0) {
            console.log('Failed to set the positions of the vertices');
            return;
        }
        
        // Draw the lines
        gl.drawArrays(gl.LINES, 0, n);
    }

}

function initVertexBuffers(gl, totalVertices) {
    var vertices = new Float32Array(coordFig);
    var n = totalVertices; // The number of vertices
  
    // Create a buffer object
    var vertexBuffer = gl.createBuffer();
    if (!vertexBuffer) {
        console.log('Failed to create the buffer object');
        return -1;
    }
  
    // Bind the buffer object to target
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    // Write date into the buffer object
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
  
    var FSIZE = vertices.BYTES_PER_ELEMENT;
  
    var a_Position = gl.getAttribLocation(gl.program, 'a_Position');
    if (a_Position < 0) {
      console.log('Failed to get the storage location of a_Position');
      return -1;
    }
  
    gl.vertexAttribPointer(a_Position, 2, gl.FLOAT, false, FSIZE * 5, 0);
    gl.enableVertexAttribArray(a_Position);  // Enable the assignment of the buffer object
  
    // Get the storage location of a_Position, assign buffer and enable
    var a_Color = gl.getAttribLocation(gl.program, 'a_Color');
    if(a_Color < 0) {
      console.log('Failed to get the storage location of a_Color');
      return -1;
    }
    
    gl.vertexAttribPointer(a_Color, 3, gl.FLOAT, false, FSIZE * 5, FSIZE * 2);
    gl.enableVertexAttribArray(a_Color);  // Enable the assignment of the buffer object
  
    return n;
}

//Funcion para dibujar las lineas del tablero
function initVertexBuffersLineas(gl, puntosLineas) {
    var vertices = new Float32Array(puntosLineas);
    var n = 2; // The number of vertices
  
    // Create a buffer object
    var vertexBuffer = gl.createBuffer();
    if (!vertexBuffer) {
      console.log('Failed to create the buffer object');
      return -1;
    }
  
    // Bind the buffer object to target
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    // Write date into the buffer object
    gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
  
    var FSIZE = vertices.BYTES_PER_ELEMENT;
  
    var a_Position = gl.getAttribLocation(gl.program, 'a_Position');
    if (a_Position < 0) {
      console.log('Failed to get the storage location of a_Position');
      return -1;
    }
  
    gl.vertexAttribPointer(a_Position, 2, gl.FLOAT, false, FSIZE * 5, 0);
    gl.enableVertexAttribArray(a_Position);  // Enable the assignment of the buffer object
  
    // Get the storage location of a_Position, assign buffer and enable
    var a_Color = gl.getAttribLocation(gl.program, 'a_Color');
    if(a_Color < 0) {
      console.log('Failed to get the storage location of a_Color');
      return -1;
    }
    
    gl.vertexAttribPointer(a_Color, 3, gl.FLOAT, false, FSIZE * 5, FSIZE * 2);
    gl.enableVertexAttribArray(a_Color);  // Enable the assignment of the buffer object
  
    return n;
  }

/*
function drawPoints(gl, g_points, a_Position) {
    // Clear <canvas>
    gl.clear(gl.COLOR_BUFFER_BIT);
    var len = g_points.length;
    for (var i = 0; i < len; i += 2) {

        if (dragging) {
            g_points[dragIndexX] = mouseCoords[0];
            g_points[dragIndexY] = mouseCoords[1];
        }
        // Pass the position of a point to a_Position variable
        gl.vertexAttrib3f(a_Position, g_points[i], g_points[i + 1], 0.0);

        // Draw a point
        gl.drawArrays(gl.POINTS, 0, 1);
    }
}
*/

function getBoardGame() {
    var contRow = 0;
  
    var max = 15;
    var min = 1;
    var row = [];
  
    //Colocar los numeros del 1-15 en el array de forma
    //random sin repetir elementos
    while (row.length < max) {
        var random = Math.floor(Math.random()*(max-min+1)+min);
        
        row.push(random)
        
        row = row.filter((item, index) => {
            return row.indexOf(item) === index
        });
      
    }
  
    //Colocar de 4 en 4 los numeros random en la matriz principal
    var temp = []
    for (var i = 0; i < max; i++) {
        contRow++;
        temp.push(row[i])
        
        if (contRow == 4) {
            boardGame.push(temp);
            temp = [];
            contRow = 0;
        }
    }
  
    //Colocar los ulitmos 3 que faltaron
    boardGame.push(temp);
  
    //Forzar a que inserte 16 al ultimo (referencia para cuadro negro)
    boardGame[3].push(16);    
    
}

function pushRGB(color) {  
    //Intercambiar el color del cuadro
    //Color rojo
    if (color == 0) {
        coordFig.push(1.0) //R
        coordFig.push(0.0) //G
        coordFig.push(0.0) //B
    //Color verde
    } else if (color == 1) {
        coordFig.push(0.0) //R
        coordFig.push(1.0) //G
        coordFig.push(0.0) //B
    //Color negro
    } else {
        coordFig.push(0.0) //R
        coordFig.push(0.0) //G
        coordFig.push(0.0) //B
    }
  }