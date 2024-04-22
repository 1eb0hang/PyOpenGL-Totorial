#version 330 core

layout (location=0) in vec4 vertPosition;

void main(){
    gl_Position = vertPosition;
}
