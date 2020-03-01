package tech.raulballeza.lesson10;

import android.opengl.GLSurfaceView;
import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private GLSurfaceView mGLSurfaceView;
    private LessonThreeRenderer mRenderer;
    View mVictimContainer;
    Button BX;
    Button BY;
    private CanvasView customCanvas;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        customCanvas = findViewById(R.id.canvas_derecho);

        mVictimContainer = findViewById(R.id.hidecontainer);
        //BX = findViewById(R.id.hideme1);
        //BY = findViewById(R.id.hideme2);
        Button B1 = findViewById(R.id.btn1);
        B1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //BX.setVisibility(View.VISIBLE);
                //BY.setVisibility(View.VISIBLE);
                customCanvas.setVisibility(View.VISIBLE);
                mVictimContainer.setVisibility(View.VISIBLE);
            }
        });

        Button B2 = findViewById(R.id.btn2);
        B2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //BX.setVisibility(View.INVISIBLE);
                //BY.setVisibility(View.INVISIBLE);
                customCanvas.setVisibility(View.INVISIBLE);
                mVictimContainer.setVisibility(View.INVISIBLE);
            }
        });

        //setContentView(R.layout.activity_main);
        mGLSurfaceView = findViewById(R.id.OpenGL1_surfaceView);
        mGLSurfaceView.setEGLContextClientVersion(2);
        mRenderer = new LessonThreeRenderer();
        mGLSurfaceView.setRenderer(mRenderer);
    }
}
