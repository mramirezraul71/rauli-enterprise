#!/usr/bin/env python3
"""
🔐 RAULI SECURITY HARDENING
Implementación de seguridad robusta y validación de entrada
"""

import os
import re
import hashlib
import hmac
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from functools import wraps
import logging
from dataclasses import dataclass
from enum import Enum
import json
import bleach
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), 'credenciales.env'))

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatLevel(Enum):
    SAFE = "safe"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"

@dataclass
class SecurityPolicy:
    name: str
    level: SecurityLevel
    description: str
    enabled: bool = True

class InputValidator:
    """Validador de entrada robusto"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Patrones de validación
        self.patterns = {
            'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            'phone': re.compile(r'^\+?1?\d{9,15}$'),
            'username': re.compile(r'^[a-zA-Z0-9_]{3,20}$'),
            'password': re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'),
            'url': re.compile(r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'),
            'numeric': re.compile(r'^\d+$'),
            'alphanumeric': re.compile(r'^[a-zA-Z0-9]+$'),
            'safe_text': re.compile(r'^[a-zA-Z0-9\s\-_.,!?@#$%&*()]+$')
        }
        
        # Listas negras
        self.blacklisted_inputs = {
            'sql_injection': [
                'DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION', 'SELECT',
                'OR 1=1', 'AND 1=1', '--', '/*', '*/', 'xp_', 'sp_',
                '<script', '</script>', 'javascript:', 'vbscript:', 'onload=', 'onerror='
            ],
            'xss': [
                '<script', 'javascript:', 'vbscript:', 'onload=', 'onerror=',
                'onclick=', 'onmouseover=', 'onfocus=', 'onblur=', 'onchange=',
                'eval(', 'alert(', 'confirm(', 'prompt('
            ],
            'path_traversal': [
                '../', '..\\', '%2e%2e%2f', '%2e%2e\\', '..%2f', '..%5c'
            ]
        }
        
        # Límites de entrada
        self.limits = {
            'max_length': {
                'username': 50,
                'email': 100,
                'password': 128,
                'message': 1000,
                'filename': 255,
                'url': 2048
            },
            'min_length': {
                'password': 8,
                'username': 3
            }
        }
    
    def validate_input(self, input_data: str, input_type: str, 
                       security_level: SecurityLevel = SecurityLevel.MEDIUM) -> Dict[str, Any]:
        """Validar entrada según tipo y nivel de seguridad"""
        
        result = {
            'valid': False,
            'sanitized': '',
            'threat_level': ThreatLevel.SAFE,
            'errors': [],
            'warnings': []
        }
        
        if not isinstance(input_data, str):
            result['errors'].append("La entrada debe ser texto")
            result['threat_level'] = ThreatLevel.DANGER
            return result
        
        # Verificar longitud
        max_len = self.limits['max_length'].get(input_type, 1000)
        min_len = self.limits['min_length'].get(input_type, 0)
        
        if len(input_data) > max_len:
            result['errors'].append(f"Longitud máxima excedida: {max_len} caracteres")
            result['threat_level'] = ThreatLevel.WARNING
        
        if len(input_data) < min_len:
            result['errors'].append(f"Longitud mínima requerida: {min_len} caracteres")
            result['threat_level'] = ThreatLevel.WARNING
        
        # Sanitización básica
        sanitized = bleach.clean(input_data, tags=[], strip=True)
        result['sanitized'] = sanitized.strip()
        
        # Verificar patrones maliciosos
        threat_detected = self._check_threats(input_data)
        if threat_detected:
            result['threat_level'] = threat_detected['level']
            result['errors'].extend(threat_detected['errors'])
        
        # Validación específica por tipo
        if input_type in self.patterns:
            pattern = self.patterns[input_type]
            if not pattern.match(sanitized):
                result['errors'].append(f"Formato inválido para {input_type}")
                result['threat_level'] = ThreatLevel.WARNING
        
        # Validación de nivel de seguridad
        if security_level == SecurityLevel.HIGH:
            if not self._high_security_validation(sanitized, input_type):
                result['errors'].append("No cumple validación de alta seguridad")
                result['threat_level'] = ThreatLevel.WARNING
        
        elif security_level == SecurityLevel.CRITICAL:
            if not self._critical_security_validation(sanitized, input_type):
                result['errors'].append("No cumple validación crítica")
                result['threat_level'] = ThreatLevel.DANGER
        
        # Si no hay errores, es válido
        if not result['errors']:
            result['valid'] = True
        
        return result
    
    def _check_threats(self, input_data: str) -> Optional[Dict[str, Any]]:
        """Verificar patrones maliciosos"""
        threats = []
        max_threat = ThreatLevel.SAFE
        
        input_lower = input_data.lower()
        
        # SQL Injection
        for pattern in self.blacklisted_inputs['sql_injection']:
            if pattern.lower() in input_lower:
                threats.append(f"Posible SQL Injection detectado: {pattern}")
                max_threat = max(max_threat, ThreatLevel.DANGER, key=lambda x: list(ThreatLevel).index(x))
        
        # XSS
        for pattern in self.blacklisted_inputs['xss']:
            if pattern.lower() in input_lower:
                threats.append(f"Posible XSS detectado: {pattern}")
                max_threat = max(max_threat, ThreatLevel.DANGER, key=lambda x: list(ThreatLevel).index(x))
        
        # Path Traversal
        for pattern in self.blacklisted_inputs['path_traversal']:
            if pattern.lower() in input_lower:
                threats.append(f"Posible Path Traversal detectado: {pattern}")
                max_threat = max(max_threat, ThreatLevel.DANGER, key=lambda x: list(ThreatLevel).index(x))
        
        if threats:
            return {
                'level': max_threat,
                'errors': threats
            }
        
        return None
    
    def _high_security_validation(self, sanitized: str, input_type: str) -> bool:
        """Validación de alta seguridad"""
        # Verificar caracteres especiales no permitidos
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        for char in dangerous_chars:
            if char in sanitized:
                return False
        
        # Verificar secuencias de escape
        escape_sequences = ['\\x', '\\u', '\\n', '\\r', '\\t']
        for seq in escape_sequences:
            if seq in sanitized:
                return False
        
        return True
    
    def _critical_security_validation(self, sanitized: str, input_type: str) -> bool:
        """Validación de seguridad crítica"""
        # Solo permitir caracteres alfanuméricos y espacios
        allowed_pattern = re.compile(r'^[a-zA-Z0-9\s]+$')
        return bool(allowed_pattern.match(sanitized))

class AuthenticationManager:
    """Gestor de autenticación seguro"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET', secrets.token_urlsafe(32))
        self.algorithm = 'HS256'
        self.token_expiry = timedelta(hours=24)
        self.refresh_expiry = timedelta(days=7)
        self.max_login_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        self.logger = logging.getLogger(__name__)
        
        # Usuarios bloqueados (en producción usar BD)
        self.locked_users = {}
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> Dict[str, str]:
        """Hash de contraseña seguro"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Usar PBKDF2 con SHA-256
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # Iteraciones
        ).hex()
        
        return {
            'hash': password_hash,
            'salt': salt
        }
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verificar contraseña"""
        computed_hash = self.hash_password(password, salt)['hash']
        return hmac.compare_digest(computed_hash, stored_hash)
    
    def generate_tokens(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Generar tokens JWT"""
        now = datetime.utcnow()
        
        # Token de acceso
        access_payload = {
            'user_id': user_data.get('user_id'),
            'username': user_data.get('username'),
            'role': user_data.get('role', 'user'),
            'iat': now,
            'exp': now + self.token_expiry,
            'type': 'access'
        }
        
        # Token de refresco
        refresh_payload = {
            'user_id': user_data.get('user_id'),
            'iat': now,
            'exp': now + self.refresh_expiry,
            'type': 'refresh'
        }
        
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': int(self.token_expiry.total_seconds())
        }
    
    def verify_token(self, token: str, token_type: str = 'access') -> Optional[Dict[str, Any]]:
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get('type') != token_type:
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expirado")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Token inválido")
            return None
    
    def is_user_locked(self, user_id: str) -> bool:
        """Verificar si usuario está bloqueado"""
        if user_id in self.locked_users:
            lock_time = self.locked_users[user_id]
            if datetime.utcnow() < lock_time:
                return True
            else:
                # Desbloquear automáticamente
                del self.locked_users[user_id]
        return False
    
    def lock_user(self, user_id: str):
        """Bloquear usuario temporalmente"""
        lock_time = datetime.utcnow() + self.lockout_duration
        self.locked_users[user_id] = lock_time
        self.logger.warning(f"Usuario {user_id} bloqueado hasta {lock_time}")

class SecurityMiddleware:
    """Middleware de seguridad para aplicaciones web"""
    
    def __init__(self):
        self.input_validator = InputValidator()
        self.auth_manager = AuthenticationManager()
        self.logger = logging.getLogger(__name__)
        
        # Políticas de seguridad
        self.policies = [
            SecurityPolicy("Input Validation", SecurityLevel.HIGH, "Validación de todas las entradas"),
            SecurityPolicy("Authentication", SecurityLevel.CRITICAL, "Autenticación robusta con JWT"),
            SecurityPolicy("Rate Limiting", SecurityLevel.MEDIUM, "Límite de peticiones por usuario"),
            SecurityPolicy("CORS Protection", SecurityLevel.MEDIUM, "Protección contra CORS"),
            SecurityPolicy("CSRF Protection", SecurityLevel.HIGH, "Protección contra CSRF"),
            SecurityPolicy("Security Headers", SecurityLevel.HIGH, "Headers de seguridad")
        ]
    
    def rate_limit_check(self, user_id: str, endpoint: str, limit: int = 100, window: int = 3600) -> bool:
        """Verificar límite de peticiones"""
        # En producción usar Redis o BD
        # Aquí simulamos con diccionario
        if not hasattr(self, '_rate_limits'):
            self._rate_limits = {}
        
        key = f"{user_id}:{endpoint}"
        now = datetime.utcnow()
        
        if key not in self._rate_limits:
            self._rate_limits[key] = []
        
        # Limpiar peticiones antiguas
        self._rate_limits[key] = [
            req_time for req_time in self._rate_limits[key]
            if (now - req_time).seconds < window
        ]
        
        # Verificar límite
        if len(self._rate_limits[key]) >= limit:
            self.logger.warning(f"Rate limit excedido para {user_id} en {endpoint}")
            return False
        
        # Registrar petición actual
        self._rate_limits[key].append(now)
        return True
    
    def add_security_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Agregar headers de seguridad"""
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }
        
        headers.update(security_headers)
        return headers
    
    def generate_csrf_token(self) -> str:
        """Generar token CSRF"""
        return secrets.token_urlsafe(32)
    
    def verify_csrf_token(self, token: str, session_token: str) -> bool:
        """Verificar token CSRF"""
        return hmac.compare_digest(token, session_token)

def require_auth(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Aquí iría la lógica de verificación de token
        # Por ahora simulamos
        token = kwargs.get('token') or args[0] if args else None
        
        if not token:
            return {'error': 'Token requerido'}, 401
        
        auth_manager = AuthenticationManager()
        payload = auth_manager.verify_token(token)
        
        if not payload:
            return {'error': 'Token inválido'}, 401
        
        # Agregar payload del usuario a kwargs
        kwargs['user_payload'] = payload
        return f(*args, **kwargs)
    
    return decorated_function

def rate_limit(limit: int = 100, window: int = 3600):
    """Decorador para rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            middleware = SecurityMiddleware()
            user_id = kwargs.get('user_id', 'anonymous')
            endpoint = f.__name__
            
            if not middleware.rate_limit_check(user_id, endpoint, limit, window):
                return {'error': 'Rate limit excedido'}, 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_input(input_type: str, security_level: SecurityLevel = SecurityLevel.MEDIUM):
    """Decorador para validación de entrada"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            validator = InputValidator()
            
            # Validar cada argumento string
            for arg_name, arg_value in kwargs.items():
                if isinstance(arg_value, str):
                    validation_result = validator.validate_input(
                        arg_value, input_type, security_level
                    )
                    
                    if not validation_result['valid']:
                        return {
                            'error': 'Entrada inválida',
                            'details': validation_result['errors']
                        }, 400
                    
                    # Reemplazar con valor sanitizado
                    kwargs[arg_name] = validation_result['sanitized']
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class SecurityAuditor:
    """Auditor de seguridad"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.audit_log = []
    
    def log_security_event(self, event_type: str, user_id: str, details: Dict[str, Any]):
        """Registrar evento de seguridad"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details,
            'severity': self._determine_severity(event_type)
        }
        
        self.audit_log.append(event)
        
        # Log al sistema de logging
        log_message = f"Security Event: {event_type} - User: {user_id} - {details}"
        if event['severity'] == 'HIGH':
            self.logger.error(log_message)
        elif event['severity'] == 'MEDIUM':
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def _determine_severity(self, event_type: str) -> str:
        """Determinar severidad del evento"""
        high_severity_events = [
            'LOGIN_FAILED', 'TOKEN_INVALID', 'RATE_LIMIT_EXCEEDED',
            'INPUT_VALIDATION_FAILED', 'CSRF_TOKEN_INVALID'
        ]
        
        medium_severity_events = [
            'LOGIN_SUCCESS', 'TOKEN_REFRESH', 'PASSWORD_CHANGE'
        ]
        
        if event_type in high_severity_events:
            return 'HIGH'
        elif event_type in medium_severity_events:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_security_report(self) -> Dict[str, Any]:
        """Generar reporte de seguridad"""
        if not self.audit_log:
            return {'message': 'No hay eventos de seguridad registrados'}
        
        # Análisis de eventos
        total_events = len(self.audit_log)
        events_by_type = {}
        events_by_severity = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for event in self.audit_log:
            event_type = event['event_type']
            severity = event['severity']
            
            events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
            events_by_severity[severity] += 1
        
        # Eventos recientes (última hora)
        recent_events = [
            event for event in self.audit_log
            if datetime.fromisoformat(event['timestamp']) > datetime.utcnow() - timedelta(hours=1)
        ]
        
        return {
            'total_events': total_events,
            'events_by_type': events_by_type,
            'events_by_severity': events_by_severity,
            'recent_events_count': len(recent_events),
            'high_risk_events': events_by_severity['HIGH'],
            'security_score': max(0, 100 - (events_by_severity['HIGH'] * 10)),
            'recommendations': self._generate_recommendations(events_by_type)
        }
    
    def _generate_recommendations(self, events_by_type: Dict[str, int]) -> List[str]:
        """Generar recomendaciones basadas en eventos"""
        recommendations = []
        
        if events_by_type.get('LOGIN_FAILED', 0) > 10:
            recommendations.append("Considerar implementar bloqueo temporal después de múltiples intentos fallidos")
        
        if events_by_type.get('RATE_LIMIT_EXCEEDED', 0) > 5:
            recommendations.append("Revisar límites de rate limiting, posible ataque de DoS")
        
        if events_by_type.get('INPUT_VALIDATION_FAILED', 0) > 5:
            recommendations.append("Revisar validación de entrada, posible intento de inyección")
        
        if events_by_type.get('TOKEN_INVALID', 0) > 3:
            recommendations.append("Investigar tokens inválidos, posible compromiso de cuentas")
        
        return recommendations

def main():
    """Función principal para testing"""
    print("🔐 RAULI Security Hardening Test")
    print("=" * 40)
    
    # Test de validación de entrada
    validator = InputValidator()
    
    test_inputs = [
        ("test@example.com", "email"),
        ("<script>alert('xss')</script>", "message"),
        ("'; DROP TABLE users; --", "username"),
        ("../../../etc/passwd", "filename"),
        ("ValidUser123", "username")
    ]
    
    print("\n📝 Test de Validación de Entrada:")
    for input_data, input_type in test_inputs:
        result = validator.validate_input(input_data, input_type)
        print(f"Input: {input_data[:30]}...")
        print(f"Valid: {result['valid']}")
        print(f"Threat: {result['threat_level'].value}")
        if result['errors']:
            print(f"Errors: {result['errors']}")
        print("-" * 30)
    
    # Test de autenticación
    auth = AuthenticationManager()
    
    print("\n🔑 Test de Autenticación:")
    user_data = {"user_id": "123", "username": "testuser", "role": "admin"}
    tokens = auth.generate_tokens(user_data)
    print(f"Tokens generados: {list(tokens.keys())}")
    
    # Verificar token
    payload = auth.verify_token(tokens['access_token'])
    print(f"Token válido: {payload is not None}")
    
    # Test de auditoría
    auditor = SecurityAuditor()
    auditor.log_security_event("LOGIN_SUCCESS", "testuser", {"ip": "127.0.0.1"})
    auditor.log_security_event("LOGIN_FAILED", "testuser", {"reason": "invalid_password"})
    
    report = auditor.generate_security_report()
    print(f"\n📊 Reporte de Seguridad:")
    print(f"Total eventos: {report.get('total_events', 0)}")
    print(f"Score seguridad: {report.get('security_score', 0)}")

if __name__ == "__main__":
    main()
