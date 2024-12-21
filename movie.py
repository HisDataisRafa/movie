import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
import tempfile
from datetime import datetime

st.title("Creador de Videos con Imágenes y Audio")

# Widgets para subir archivos
uploaded_images = st.file_uploader("Sube tus imágenes", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
uploaded_audios = st.file_uploader("Sube tus archivos de audio", type=['mp3', 'wav'], accept_multiple_files=True)

if st.button("Crear Video") and uploaded_images and uploaded_audios:
    if len(uploaded_images) != len(uploaded_audios):
        st.error("El número de imágenes debe ser igual al número de audios")
    else:
        try:
            with st.spinner("Creando video..."):
                # Crear directorio temporal
                temp_dir = tempfile.mkdtemp()
                
                # Guardar archivos temporalmente
                image_paths = []
                audio_paths = []
                
                for img in uploaded_images:
                    temp_path = os.path.join(temp_dir, img.name)
                    with open(temp_path, 'wb') as f:
                        f.write(img.getbuffer())
                    image_paths.append(temp_path)
                
                for aud in uploaded_audios:
                    temp_path = os.path.join(temp_dir, aud.name)
                    with open(temp_path, 'wb') as f:
                        f.write(aud.getbuffer())
                    audio_paths.append(temp_path)
                
                # Crear clips de video
                video_clips = []
                for img_path, aud_path in zip(image_paths, audio_paths):
                    audio = AudioFileClip(aud_path)
                    video_clip = ImageClip(img_path).with_duration(audio.duration)
                    video_clip = video_clip.with_audio(audio)
                    video_clips.append(video_clip)
                
                # Concatenar clips
                final_video = concatenate_videoclips(video_clips)
                
                # Guardar video final
                output_path = os.path.join(temp_dir, "video_final.mp4")
                final_video.write_videofile(
                    output_path,
                    fps=24,
                    codec='libx264',
                    audio_codec='aac'
                )
                
                # Leer el video para descarga
                with open(output_path, 'rb') as f:
                    video_bytes = f.read()
                
                # Botón de descarga
                st.download_button(
                    label="Descargar Video",
                    data=video_bytes,
                    file_name="video_final.mp4",
                    mime="video/mp4"
                )
                
                # Limpiar
                for clip in video_clips:
                    clip.close()
                final_video.close()
                
        except Exception as e:
            st.error(f"Error al crear el video: {str(e)}")

st.markdown("""
### Instrucciones:
1. Sube tus imágenes (.png, .jpg, .jpeg)
2. Sube tus archivos de audio (.mp3, .wav)
3. Asegúrate de tener el mismo número de imágenes y audios
4. Haz clic en "Crear Video"
5. Espera a que se procese y descarga tu video
""")
