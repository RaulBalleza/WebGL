package tech.raulballeza.lesson9;

import android.content.Context;
import android.opengl.GLES20;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;
import java.nio.IntBuffer;
import java.nio.ShortBuffer;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class CubeRefinado {

    public static final int INT_BYTES = 4;

    // Originales: Gradientes entre las caras
    // Cube vertices
/*    private static final float VERTICES[] = {
            -0.5f, -0.5f, -0.5f,
            0.5f, -0.5f, -0.5f,
            0.5f, 0.5f, -0.5f,
            -0.5f, 0.5f, -0.5f,
            -0.5f, -0.5f, 0.5f,
            0.5f, -0.5f, 0.5f,
            0.5f, 0.5f, 0.5f,
            -0.5f, 0.5f, 0.5f
    };

    // Vertex colors.
    private static final float COLORS[] = {
            0.0f, 1.0f, 1.0f, 1.0f,
            1.0f, 0.0f, 0.0f, 1.0f,
            1.0f, 1.0f, 0.0f, 1.0f,
            0.0f, 1.0f, 0.0f, 1.0f,
            0.0f, 0.0f, 1.0f, 1.0f,
            1.0f, 0.0f, 1.0f, 1.0f,
            1.0f, 1.0f, 1.0f, 1.0f,
            0.0f, 1.0f, 1.0f, 1.0f,
    };


    // Order to draw vertices as triangles.
    private static final byte INDICES[] = {
            0, 1, 3, 3, 1, 2, // Front face.
            0, 1, 4, 4, 5, 1, // Bottom face.
            1, 2, 5, 5, 6, 2, // Right face.
            2, 3, 6, 6, 7, 3, // Top face.
            3, 7, 4, 4, 3, 0, // Left face.
            4, 5, 7, 7, 6, 5, // Rear face.
    };

*/

    // Modificados: Un color por cara, mas colorer al utilizar TRIANGLES en vez de TRIANGLE_STRIP
    // Cube vertices
    private static final float VERTICES[] = {
            -0.5f, -0.5f, -0.5f,
             0.5f, -0.5f, -0.5f,
             0.5f, 0.5f, -0.5f,
            -0.5f, 0.5f, -0.5f,

            -0.5f, -0.5f, 0.5f,
             0.5f, -0.5f, 0.5f,
             0.5f,  0.5f, 0.5f,
            -0.5f,  0.5f, 0.5f,

            -0.5f, -0.5f, -0.5f,
            -0.5f, -0.5f,  0.5f,
            -0.5f, 0.5f,  0.5f,
            -0.5f, 0.5f, -0.5f,

            0.5f, -0.5f, -0.5f,
            0.5f, -0.5f,  0.5f,
            0.5f, 0.5f,  0.5f,
            0.5f, 0.5f, -0.5f,

            -0.5f, -0.5f, -0.5f,
            -0.5f, -0.5f,  0.5f,
            0.5f,  -0.5f,  0.5f,
            0.5f,  -0.5f, -0.5f,

            -0.5f, 0.5f, -0.5f,
            -0.5f, 0.5f,  0.5f,
            0.5f,  0.5f,  0.5f,
            0.5f,  0.5f, -0.5f,

            //-0.5f, -0.5f, 0.5f,
            //0.5f, -0.5f, 0.5f,
            //0.5f, 0.5f, 0.5f,
            //-0.5f, 0.5f, 0.5f
    };

    // Vertex colors.
    private static final float COLORS[] = {
            0.0f, 1.0f, 1.0f, 1.0f,
            0.0f, 1.0f, 1.0f, 1.0f,
            0.0f, 1.0f, 1.0f, 1.0f,
            0.0f, 1.0f, 1.0f, 1.0f,

            1.0f, 0.0f, 0.0f, 1.0f,
            1.0f, 0.0f, 0.0f, 1.0f,
            1.0f, 0.0f, 0.0f, 1.0f,
            1.0f, 0.0f, 0.0f, 1.0f,

            1.0f, 0.0f, 1.0f, 1.0f,
            1.0f, 0.0f, 1.0f, 1.0f,
            1.0f, 0.0f, 1.0f, 1.0f,
            1.0f, 0.0f, 1.0f, 1.0f,

            0.0f, 1.0f, 0.0f, 1.0f,
            0.0f, 1.0f, 0.0f, 1.0f,
            0.0f, 1.0f, 0.0f, 1.0f,
            0.0f, 1.0f, 0.0f, 1.0f,

            0.0f, 0.0f, 1.0f, 1.0f,
            0.0f, 0.0f, 1.0f, 1.0f,
            0.0f, 0.0f, 1.0f, 1.0f,
            0.0f, 0.0f, 1.0f, 1.0f,

            1.0f, 1.0f, 0.0f, 1.0f,
            1.0f, 1.0f, 0.0f, 1.0f,
            1.0f, 1.0f, 0.0f, 1.0f,
            1.0f, 1.0f, 0.0f, 1.0f,

    };


    // Order to draw vertices as triangles.
/*    private static final byte INDICES[] = {
            0, 1,  3,  3, 1,  2,   // Front face.
            4, 5,  7,  7, 5,  6,   // Back face.
            8, 9, 11, 11, 9, 10, // Left face.
            12, 13, 15, 15, 13, 14, // Right face.
            16, 17, 19, 19, 17, 18, // Bottom face.
            20, 21, 23, 23, 21, 22, // Top face.

            //0, 1, 4, 4, 5, 1, // Bottom face.
            //1, 2, 5, 5, 6, 2, // Right face.
            //2, 3, 6, 6, 7, 3, // Top face.
            //3, 7, 4, 4, 3, 0, // Left face.
            //4, 5, 7, 7, 6, 5, // Rear face.
    };
*/


    // Number of coordinates per vertex in {@link VERTICES}.
    private static final int COORDS_PER_VERTEX = 3;

    // Number of values per colors in {@link COLORS}.
    private static final int VALUES_PER_COLOR = 4;

    // Vertex size in bytes.
    private final int VERTEX_STRIDE = COORDS_PER_VERTEX * 4;

    // Color size in bytes.
    private final int COLOR_STRIDE = VALUES_PER_COLOR * 4;

    /** Shader code for the vertex. */
    private static final String VERTEX_SHADER_CODE =
                    "uniform mat4 uMVPMatrix;" +
                    "attribute vec4 vPosition;" +
                    "attribute vec4 vColor;" +
                    "varying vec4 _vColor;" +
                    "void main() {" +
                    "  _vColor = vColor;" +
                    "  gl_Position = uMVPMatrix * vPosition;" +
                    "}";

    /** Shader code for the fragment. */
    private static final String FRAGMENT_SHADER_CODE =
                    "precision mediump float;" +
                    "varying vec4 _vColor;" +
                    "void main() {" +
                    "  gl_FragColor = _vColor;" +
                    "}";


    private final FloatBuffer mVertexBuffer;
    private final FloatBuffer mColorBuffer;
    //private final IntBuffer mIndexBuffer;
    private final ShortBuffer mIndexBuffer;

    private final int mProgram;
    private final int mPositionHandle;
    private final int mColorHandle;
    private final int mMVPMatrixHandle;
    private FloatBuffer verticesBuffer;
    private ShortBuffer facesBuffer;
    public List<String> verticesList;
    public  List<String> facesList;
    public int Lineas;

    int TVertices;
    int TCaras;


    public CubeRefinado(Context context) {
        TVertices = 0;
        TCaras=0;


        verticesList = new ArrayList<>();
        facesList = new ArrayList<>();
        Lineas=0;

        //Toast.makeText(CTXX,"Puttito",Toast.LENGTH_SHORT).show();

        String line;
        StringBuffer buf = new StringBuffer();
        //InputStream is = context.getResources().openRawResource(R.raw.torusmejx);
        InputStream is = context.getResources().openRawResource(R.raw.cubo_simple);
        //InputStream is = context.getResources().openRawResource(R.raw.icosaedro_final);
        //InputStream is = context.getResources().openRawResource(R.raw.cilindro);
        //InputStream is = context.getResources().openRawResource(R.raw.cono);
        //InputStream is = context.getResources().openRawResource(R.raw.dona);
        //InputStream is = context.getResources().openRawResource(R.raw.rounded_cube);
        //InputStream is = context.getResources().openRawResource(R.raw.chango_marango);
        //InputStream is = context.getResources().openRawResource(R.raw.avioneta);




        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            if (is != null) {
                while ((line = reader.readLine()) != null) {
                    Lineas++;
                    buf.append(line+ "\n" );
                    if(line.startsWith("v ")) {
                        verticesList.add(line);
                        TVertices++;
                    } else if(line.startsWith("f ")) {
                        facesList.add(line);
                        TCaras++;
                    }

                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try { is.close(); } catch (Throwable ignore) {}
        }

        //Toast.makeText(context, buf.toString(), Toast.LENGTH_LONG).show();
        //Toast.makeText(context, facesList.toString(), Toast.LENGTH_LONG).show();
        //Log.d ("XXX",""+facesList.toString());
        //Log.d ("XXX",""+verticesList.toString());
        Log.d ("XXX","Total Vertices "+TVertices);
        Log.d ("XXX","Total Caras "+TCaras);
        Log.d ("XXX","VerticesList"+verticesList.size());



        //ByteBuffer byteBuffer = ByteBuffer.allocateDirect(VERTICES.length * 4);
        ByteBuffer byteBuffer = ByteBuffer.allocateDirect(verticesList.size()* 3 * 4);
        byteBuffer.order(ByteOrder.nativeOrder());
        mVertexBuffer = byteBuffer.asFloatBuffer();
        //mVertexBuffer.put(VERTICES);
        /*String C="";
        int T=0; */

        for(String vertex: verticesList) {
            String coords[] = vertex.split(" ");
            float x = Float.parseFloat(coords[1]);
            float y = Float.parseFloat(coords[2]);
            float z = Float.parseFloat(coords[3]);
            //T++;
            mVertexBuffer.put(x);
            mVertexBuffer.put(y);
            mVertexBuffer.put(z);
            Log.d ("XXX","X Y Z "+x+" "+y+" "+ z);
        }

        //Log.d ("XXX","Vertices Cargados"+T);*/

        mVertexBuffer.position(0);




        //byteBuffer = ByteBuffer.allocateDirect(COLORS.length * 4);
        byteBuffer = ByteBuffer.allocateDirect(facesList.size() * 3 * INT_BYTES);
        byteBuffer.order(ByteOrder.nativeOrder());
        mColorBuffer = byteBuffer.asFloatBuffer();
        //mColorBuffer.put(COLORS);
        Random r = new Random();
        for(String face: facesList) {
            // Genera un color aleatorio
            float value1 = r.nextFloat();//random.nextFloat();
            float value2 = r.nextFloat();//random.nextFloat();
            float value3 = r.nextFloat();//random.nextFloat();

            mColorBuffer.put(value1);
            mColorBuffer.put(value2);
            mColorBuffer.put(value3);
        }
        mColorBuffer.position(0);

        //ByteBuffer byteBuffer2 = ByteBuffer.allocateDirect(facesList.size() * 3 * 4);

                //mIndexBuffer = ByteBuffer.allocateDirect(INDICES.length);

        byteBuffer = ByteBuffer.allocateDirect(facesList.size()* 3 * INT_BYTES);
        byteBuffer.order(ByteOrder.nativeOrder());
        //mIndexBuffer = byteBuffer.asIntBuffer();
        //mIndexBuffer = byteBuffer.asIntBuffer();
        mIndexBuffer = byteBuffer.asShortBuffer();



        //mIndexBuffer.put(INDICES);
        for(String face: facesList) {
            String vertexIndices[] = face.split(" ");
            /*byte vertex1 = (byte) Short.parseShort(vertexIndices[1]);
            byte vertex2 = (byte) Short.parseShort(vertexIndices[2]);
            byte vertex3 = (byte) Short.parseShort(vertexIndices[3]);
            mIndexBuffer.put((byte) (vertex1 - 1));
            mIndexBuffer.put((byte) (vertex2 - 1));
            mIndexBuffer.put((byte) (vertex3 - 1));*/

            /*int vertex1 = Integer.parseInt(vertexIndices[1]);
            int vertex2 = Integer.parseInt(vertexIndices[2]);
            int vertex3 = Integer.parseInt(vertexIndices[3]);*/

            short vertex1 = Short.parseShort(vertexIndices[1]);
            short vertex2 = Short.parseShort(vertexIndices[2]);
            short vertex3 = Short.parseShort(vertexIndices[3]);
            mIndexBuffer.put((short) (vertex1 - 1));
            mIndexBuffer.put((short) (vertex2 - 1));
            mIndexBuffer.put((short) (vertex3 - 1));


            Log.d ("XXX","V1 V2 V3 ["+vertex1+" "+vertex2+" "+ vertex3+"]");
        }
        mIndexBuffer.position(0);

        mProgram = GLES20.glCreateProgram();
        GLES20.glAttachShader(mProgram, loadShader(GLES20.GL_VERTEX_SHADER, VERTEX_SHADER_CODE));
        GLES20.glAttachShader(mProgram, loadShader(GLES20.GL_FRAGMENT_SHADER, FRAGMENT_SHADER_CODE));
        GLES20.glLinkProgram(mProgram);

        mPositionHandle = GLES20.glGetAttribLocation(mProgram, "vPosition");
        mColorHandle = GLES20.glGetAttribLocation(mProgram, "vColor");
        mMVPMatrixHandle = GLES20.glGetUniformLocation(mProgram, "uMVPMatrix");
    }

    /**
     * Encapsulates the OpenGL ES instructions for drawing this shape.
     *
     * @param mvpMatrix The Model View Project matrix in which to draw this shape
     */
    public void draw(float[] mvpMatrix) {
        // Add program to OpenGL environment.
        GLES20.glUseProgram(mProgram);

        // Prepare the cube coordinate data.
        GLES20.glEnableVertexAttribArray(mPositionHandle);
        GLES20.glVertexAttribPointer(
                mPositionHandle, 3, GLES20.GL_FLOAT, false, VERTEX_STRIDE, mVertexBuffer);

        // Prepare the cube color data.
        GLES20.glEnableVertexAttribArray(mColorHandle);
        GLES20.glVertexAttribPointer(
                mColorHandle, 4, GLES20.GL_FLOAT, false, COLOR_STRIDE, mColorBuffer);

        // Apply the projection and view transformation.
        GLES20.glUniformMatrix4fv(mMVPMatrixHandle, 1, false, mvpMatrix, 0);

        // Draw the cube.
        //GLES20.glDrawElements(GLES20.GL_TRIANGLES, INDICES.length, GLES20.GL_UNSIGNED_BYTE, mIndexBuffer);
        //GLES20.glDrawElements(GLES20.GL_TRIANGLES, TCaras*3, GLES20.GL_UNSIGNED_BYTE, mIndexBuffer);
        //GLES20.glDrawElements(GLES20.GL_TRIANGLES, TCaras*3, GLES20.GL_INT, mIndexBuffer);
        GLES20.glDrawElements(GLES20.GL_TRIANGLES, TCaras*3, GLES20.GL_UNSIGNED_SHORT, mIndexBuffer);

        //GLES20.glDrawElements(GLES20.GL_TRIANGLES, INDICES.length, GLES20.GL_INT, mIndexBuffer);
        //GLES20.glDrawElements(GLES20.GL_TRIANGLE_STRIP, INDICES.length, GLES20.GL_UNSIGNED_BYTE, mIndexBuffer);

        // Disable vertex arrays.
        GLES20.glDisableVertexAttribArray(mPositionHandle);
        GLES20.glDisableVertexAttribArray(mColorHandle);
    }

    /** Loads the provided shader in the program. */
    private static int loadShader(int type, String shaderCode){
        int shader = GLES20.glCreateShader(type);

        GLES20.glShaderSource(shader, shaderCode);
        GLES20.glCompileShader(shader);

        return shader;
    }


}
