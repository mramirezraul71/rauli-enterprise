#!/usr/bin/env python3
"""
👁️ MÓDULO DE VISIÓN - RAULI Vision System
Sistema completo de visión por computadora con cámara en tiempo real
"""

import cv2
import numpy as np
import streamlit as st
import threading
import time
import os
from datetime import datetime
import json
from PIL import Image
import io
import base64

class RAULIVisionSystem:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.detection_results = {}
        self.vision_history = []
        
        # Directorios
        self.base_dir = r'C:\RAULI_CORE'
        self.vision_dir = os.path.join(self.base_dir, 'vision_data')
        self.captures_dir = os.path.join(self.vision_dir, 'captures')
        self.detections_dir = os.path.join(self.vision_dir, 'detections')
        
        # Crear directorios
        for dir_path in [self.vision_dir, self.captures_dir, self.detections_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # Configuración de cámara
        self.camera_config = {
            'resolution': (640, 480),
            'fps': 30,
            'brightness': 0.5,
            'contrast': 0.5,
            'saturation': 0.5
        }
        
        # Modelos de detección
        self.detection_models = {
            'face': self.load_face_detector(),
            'objects': self.load_object_detector(),
            'text': self.load_text_detector()
        }
        
        print("👁️ RAULI Vision System inicializado")
    
    def load_face_detector(self):
        """Cargar detector de rostros"""
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            return face_cascade
        except Exception as e:
            print(f"❌ Error cargando detector de rostros: {e}")
            return None
    
    def load_object_detector(self):
        """Cargar detector de objetos"""
        try:
            # Placeholder para detector de objetos (puede ser YOLO, etc.)
            return "object_detector_placeholder"
        except Exception as e:
            print(f"❌ Error cargando detector de objetos: {e}")
            return None
    
    def load_text_detector(self):
        """Cargar detector de texto"""
        try:
            # Placeholder para OCR (puede ser Tesseract, etc.)
            return "text_detector_placeholder"
        except Exception as e:
            print(f"❌ Error cargando detector de texto: {e}")
            return None
    
    def initialize_camera(self, camera_id=0):
        """Inicializar cámara"""
        try:
            self.camera = cv2.VideoCapture(camera_id)
            
            if not self.camera.isOpened():
                raise Exception("No se pudo abrir la cámara")
            
            # Configurar resolución
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_config['resolution'][0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_config['resolution'][1])
            self.camera.set(cv2.CAP_PROP_FPS, self.camera_config['fps'])
            
            print(f"✅ Cámara inicializada (ID: {camera_id})")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando cámara: {e}")
            return False
    
    def capture_frame(self):
        """Capturar frame de la cámara"""
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                self.current_frame = frame.copy()
                return frame
        return None
    
    def detect_faces(self, frame):
        """Detectar rostros en el frame"""
        if self.detection_models['face'] is None:
            return []
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detection_models['face'].detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            return faces
        except Exception as e:
            print(f"❌ Error detectando rostros: {e}")
            return []
    
    def detect_objects(self, frame):
        """Detectar objetos en el frame"""
        # Placeholder para detección de objetos
        return []
    
    def detect_text(self, frame):
        """Detectar texto en el frame"""
        # Placeholder para OCR
        return []
    
    def process_frame(self, frame):
        """Procesar frame completo con todas las detecciones"""
        if frame is None:
            return None
        
        processed_frame = frame.copy()
        timestamp = datetime.now()
        
        # Detectar rostros
        faces = self.detect_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(processed_frame, 'Rostro', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Detectar objetos
        objects = self.detect_objects(frame)
        for obj in objects:
            # Placeholder para dibujar objetos
            pass
        
        # Detectar texto
        text = self.detect_text(frame)
        for txt in text:
            # Placeholder para dibujar texto
            pass
        
        # Guardar resultados
        detection_data = {
            'timestamp': timestamp.isoformat(),
            'faces_detected': len(faces),
            'objects_detected': len(objects),
            'text_detected': len(text),
            'frame_shape': frame.shape
        }
        
        self.detection_results = detection_data
        self.vision_history.append(detection_data)
        
        return processed_frame
    
    def start_continuous_capture(self):
        """Iniciar captura continua"""
        if not self.initialize_camera():
            return False
        
        self.is_running = True
        
        def capture_loop():
            while self.is_running:
                frame = self.capture_frame()
                if frame is not None:
                    processed_frame = self.process_frame(frame)
                    self.current_frame = processed_frame
                time.sleep(1/self.camera_config['fps'])
        
        capture_thread = threading.Thread(target=capture_loop, daemon=True)
        capture_thread.start()
        
        print("🎥 Captura continua iniciada")
        return True
    
    def stop_continuous_capture(self):
        """Detener captura continua"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        print("⏹️ Captura detenida")
    
    def save_capture(self, frame, filename=None):
        """Guardar captura"""
        if filename is None:
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        filepath = os.path.join(self.captures_dir, filename)
        cv2.imwrite(filepath, frame)
        
        print(f"📸 Captura guardada: {filepath}")
        return filepath
    
    def get_frame_as_image(self, frame):
        """Convertir frame a PIL Image"""
        if frame is None:
            return None
        
        # Convertir BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        return pil_image
    
    def get_frame_as_bytes(self, frame):
        """Convertir frame a bytes para Streamlit"""
        if frame is None:
            return None
        
        pil_image = self.get_frame_as_image(frame)
        if pil_image is None:
            return None
        
        # Convertir a bytes
        img_buffer = io.BytesIO()
        pil_image.save(img_buffer, format='JPEG')
        img_bytes = img_buffer.getvalue()
        
        return img_bytes
    
    def get_vision_stats(self):
        """Obtener estadísticas de visión"""
        if not self.vision_history:
            return {}
        
        total_frames = len(self.vision_history)
        total_faces = sum(item['faces_detected'] for item in self.vision_history)
        total_objects = sum(item['objects_detected'] for item in self.vision_history)
        total_text = sum(item['text_detected'] for item in self.vision_history)
        
        return {
            'total_frames_processed': total_frames,
            'total_faces_detected': total_faces,
            'total_objects_detected': total_objects,
            'total_text_detected': total_text,
            'avg_faces_per_frame': total_faces / total_frames if total_frames > 0 else 0,
            'capture_rate': self.camera_config['fps'],
            'resolution': self.camera_config['resolution']
        }

# Integración con Streamlit
def create_vision_interface():
    """Crear interfaz de visión para Streamlit"""
    
    st.title("👁️ RAULI Vision System")
    st.markdown("---")
    
    # Inicializar sistema de visión
    if 'vision_system' not in st.session_state:
        st.session_state.vision_system = RAULIVisionSystem()
    
    vision_system = st.session_state.vision_system
    
    # Controles principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎥 Iniciar Cámara", key="start_camera"):
            if vision_system.start_continuous_capture():
                st.success("✅ Cámara iniciada")
            else:
                st.error("❌ Error al iniciar cámara")
    
    with col2:
        if st.button("⏹️ Detener Cámara", key="stop_camera"):
            vision_system.stop_continuous_capture()
            st.success("⏹️ Cámara detenida")
    
    with col3:
        if st.button("📸 Capturar Foto", key="capture_photo"):
            frame = vision_system.capture_frame()
            if frame is not None:
                filepath = vision_system.save_capture(frame)
                st.success(f"📸 Foto guardada: {filepath}")
            else:
                st.error("❌ Error al capturar foto")
    
    # Configuración
    st.markdown("### ⚙️ Configuración de Cámara")
    
    col1, col2 = st.columns(2)
    
    with col1:
        resolution = st.selectbox(
            "Resolución",
            [(640, 480), (1280, 720), (1920, 1080)],
            index=0
        )
        vision_system.camera_config['resolution'] = resolution
    
    with col2:
        fps = st.slider("FPS", 10, 60, 30)
        vision_system.camera_config['fps'] = fps
    
    # Vista en tiempo real
    st.markdown("### 📹 Vista en Tiempo Real")
    
    # Placeholder para video
    video_placeholder = st.empty()
    
    # Actualizar frame continuamente
    if vision_system.is_running and vision_system.current_frame is not None:
        frame_bytes = vision_system.get_frame_as_bytes(vision_system.current_frame)
        if frame_bytes:
            video_placeholder.image(frame_bytes, channels="BGR", use_container_width=True)
    
    # Estadísticas
    st.markdown("### 📊 Estadísticas de Visión")
    
    stats = vision_system.get_vision_stats()
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Frames Procesados", stats.get('total_frames_processed', 0))
        
        with col2:
            st.metric("Rostros Detectados", stats.get('total_faces_detected', 0))
        
        with col3:
            st.metric("Objetos Detectados", stats.get('total_objects_detected', 0))
        
        with col4:
            st.metric("FPS", stats.get('capture_rate', 0))
    
    # Galería de capturas
    st.markdown("### 🖼️ Galería de Capturas")
    
    captures_dir = vision_system.captures_dir
    if os.path.exists(captures_dir):
        capture_files = [f for f in os.listdir(captures_dir) if f.endswith(('.jpg', '.png'))]
        
        if capture_files:
            # Mostrar últimas 6 capturas
            recent_captures = capture_files[-6:]
            
            cols = st.columns(3)
            for i, capture_file in enumerate(recent_captures):
                with cols[i % 3]:
                    filepath = os.path.join(captures_dir, capture_file)
                    st.image(filepath, caption=capture_file, use_container_width=True)
        else:
            st.info("📸 No hay capturas guardadas")

# Función principal para testing
def main():
    """Función principal para testing del módulo de visión"""
    print("👁️ Iniciando RAULI Vision System...")
    
    vision_system = RAULIVisionSystem()
    
    # Probar inicialización de cámara
    if vision_system.initialize_camera():
        print("✅ Cámara inicializada correctamente")
        
        # Capturar algunos frames
        for i in range(5):
            frame = vision_system.capture_frame()
            if frame is not None:
                processed_frame = vision_system.process_frame(frame)
                vision_system.save_capture(processed_frame, f"test_capture_{i}.jpg")
                print(f"📸 Captura {i+1} guardada")
            time.sleep(1)
        
        # Mostrar estadísticas
        stats = vision_system.get_vision_stats()
        print(f"📊 Estadísticas: {stats}")
        
        # Detener cámara
        vision_system.stop_continuous_capture()
        print("⏹️ Cámara detenida")
    else:
        print("❌ No se pudo inicializar la cámara")

if __name__ == "__main__":
    main()
