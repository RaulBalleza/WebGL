package tech.raulballeza.lesson11;

import android.opengl.GLSurfaceView;
//import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private GLSurfaceView mGLSurfaceView;
    private LessonThreeRenderer mRenderer;
    View mVictimContainer;
    Button BX;
    Button BY;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mVictimContainer = findViewById(R.id.hidecontainer);
        BX = findViewById(R.id.hideme1);
        BY = findViewById(R.id.hideme2);
        Button B1 = findViewById(R.id.btn1);
        B1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                BX.setVisibility(View.VISIBLE);
                BY.setVisibility(View.VISIBLE);
                mVictimContainer.setVisibility(View.VISIBLE);
            }
        });

        Button B2 = findViewById(R.id.btn2);
        B2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                BX.setVisibility(View.INVISIBLE);
                BY.setVisibility(View.INVISIBLE);
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
