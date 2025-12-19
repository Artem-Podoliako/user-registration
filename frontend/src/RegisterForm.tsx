import { useState, FormEvent } from 'react';
import { registerUser, ErrorResponse } from './api';
import axios from 'axios';

export default function RegisterForm() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
    setLoading(true);

    try {
      const response = await registerUser(login, password);
      setMessage(response.message);
      setLogin('');
      setPassword('');
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const errorData = err.response.data as ErrorResponse;
        if (typeof errorData.detail === 'string') {
          setError(errorData.detail);
        } else if (Array.isArray(errorData.detail)) {
          const errorMessages = errorData.detail.map(
            (item) => `${item.loc.join('.')}: ${item.msg}`
          );
          setError(errorMessages.join(', '));
        } else {
          setError('Ошибка регистрации');
        }
      } else {
        setError('Ошибка сети. Пожалуйста, попробуйте снова.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.wrapper}>
      <div style={styles.container}>
        {/* Декоративные элементы */}
        <div style={styles.glow1} />
        <div style={styles.glow2} />
        <div style={styles.glow3} />
        
        <div style={styles.content}>
          {/* Верхняя декоративная линия */}
          <div style={styles.topLine} />
          
          <div style={styles.header}>
            <div style={styles.titleWrapper}>
              <h1 style={styles.title}>
                <span style={styles.titleGradient}>Регистрация</span>
              </h1>
              <div style={styles.titleUnderline} />
            </div>
            <p style={styles.subtitle}>Создайте новый аккаунт</p>
          </div>

          <form onSubmit={handleSubmit} style={styles.form}>
            <div style={styles.formGroup}>
              <label htmlFor="login" style={styles.label}>
                Логин
              </label>
              <div style={styles.inputWrapper}>
                <input
                  id="login"
                  type="text"
                  value={login}
                  onChange={(e) => setLogin(e.target.value)}
                  onFocus={() => setFocusedField('login')}
                  onBlur={() => setFocusedField(null)}
                  required
                  minLength={3}
                  maxLength={32}
                  pattern="[a-zA-Z0-9._-]+"
                  style={{
                    ...styles.input,
                    ...(focusedField === 'login' ? styles.inputFocused : {}),
                  }}
                  placeholder="3-32 символа, буквы/цифры/._-"
                />
                <div style={{
                  ...styles.inputUnderline,
                  ...(focusedField === 'login' ? styles.inputUnderlineActive : {}),
                }} />
                {focusedField === 'login' && <div style={styles.inputGlow} />}
              </div>
            </div>

            <div style={styles.formGroup}>
              <label htmlFor="password" style={styles.label}>
                Пароль
              </label>
              <div style={styles.inputWrapper}>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onFocus={() => setFocusedField('password')}
                  onBlur={() => setFocusedField(null)}
                  required
                  minLength={8}
                  style={{
                    ...styles.input,
                    ...(focusedField === 'password' ? styles.inputFocused : {}),
                  }}
                  placeholder="Мин. 8 символов, заглавная, строчная, цифра, спецсимвол"
                />
                <div style={{
                  ...styles.inputUnderline,
                  ...(focusedField === 'password' ? styles.inputUnderlineActive : {}),
                }} />
                {focusedField === 'password' && <div style={styles.inputGlow} />}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              style={loading ? { ...styles.button, ...styles.buttonDisabled } : styles.button}
            >
              {loading ? (
                <>
                  <span style={styles.buttonSpinner} />
                  Регистрация...
                </>
              ) : (
                'Зарегистрироваться'
              )}
            </button>
          </form>

          {message && (
            <div style={styles.successMessage}>
              {message}
            </div>
          )}
          {error && (
            <div style={styles.errorMessage}>
              {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  wrapper: {
    minHeight: '100vh',
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    position: 'relative',
    zIndex: 1,
  },
  container: {
    width: '100%',
    maxWidth: '640px',
    position: 'relative',
    zIndex: 2,
  },
  glow1: {
    position: 'absolute',
    top: '-30%',
    left: '-20%',
    width: '400px',
    height: '400px',
    background: 'radial-gradient(circle, rgba(60, 60, 90, 0.15) 0%, transparent 70%)',
    borderRadius: '50%',
    animation: 'float 25s ease-in-out infinite',
    zIndex: 0,
    filter: 'blur(40px)',
  },
  glow2: {
    position: 'absolute',
    bottom: '-30%',
    right: '-20%',
    width: '400px',
    height: '400px',
    background: 'radial-gradient(circle, rgba(40, 40, 70, 0.12) 0%, transparent 70%)',
    borderRadius: '50%',
    animation: 'float 30s ease-in-out infinite reverse',
    zIndex: 0,
    filter: 'blur(50px)',
  },
  glow3: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '300px',
    height: '300px',
    background: 'radial-gradient(circle, rgba(30, 30, 50, 0.1) 0%, transparent 70%)',
    borderRadius: '50%',
    animation: 'pulse 15s ease-in-out infinite',
    zIndex: 0,
    filter: 'blur(60px)',
  },
  content: {
    background: 'rgba(5, 5, 10, 0.75)',
    backdropFilter: 'blur(30px)',
    WebkitBackdropFilter: 'blur(30px)',
    border: '1px solid rgba(255, 255, 255, 0.08)',
    borderRadius: '20px',
    padding: '56px 48px',
    boxShadow: `
      0 20px 60px rgba(0, 0, 0, 0.6),
      inset 0 1px 0 rgba(255, 255, 255, 0.05),
      0 0 0 1px rgba(255, 255, 255, 0.03)
    `,
    position: 'relative',
    overflow: 'hidden',
  },
  topLine: {
    position: 'absolute',
    top: 0,
    left: '10%',
    right: '10%',
    height: '1px',
    background: 'linear-gradient(to right, transparent, rgba(255, 255, 255, 0.1), transparent)',
  },
  header: {
    textAlign: 'center',
    marginBottom: '48px',
  },
  titleWrapper: {
    position: 'relative',
    display: 'inline-block',
    marginBottom: '16px',
  },
  title: {
    fontSize: '42px',
    fontWeight: '700',
    letterSpacing: '-1px',
    margin: 0,
    lineHeight: '1.1',
  },
  titleGradient: {
    background: 'linear-gradient(135deg, #e0e0e0 0%, #a0a0a0 50%, #808080 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  titleUnderline: {
    position: 'absolute',
    bottom: '-8px',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '60px',
    height: '2px',
    background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent)',
  },
  subtitle: {
    fontSize: '15px',
    color: 'rgba(255, 255, 255, 0.5)',
    fontWeight: '400',
    letterSpacing: '0.5px',
    marginTop: '8px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '32px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  label: {
    fontSize: '11px',
    fontWeight: '600',
    color: 'rgba(255, 255, 255, 0.7)',
    textTransform: 'uppercase',
    letterSpacing: '1.5px',
    marginBottom: '4px',
  },
  inputWrapper: {
    position: 'relative',
  },
  input: {
    width: '100%',
    padding: '18px 22px',
    background: 'rgba(0, 0, 0, 0.4)',
    border: '1px solid rgba(255, 255, 255, 0.08)',
    borderRadius: '12px',
    fontSize: '16px',
    color: '#ffffff',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    outline: 'none',
    fontFamily: 'inherit',
  },
  inputFocused: {
    background: 'rgba(0, 0, 0, 0.6)',
    borderColor: 'rgba(255, 255, 255, 0.2)',
    boxShadow: `
      0 0 0 3px rgba(255, 255, 255, 0.05),
      inset 0 1px 2px rgba(255, 255, 255, 0.05)
    `,
    transform: 'translateY(-1px)',
  },
  inputUnderline: {
    position: 'absolute',
    bottom: 0,
    left: '50%',
    transform: 'translateX(-50%)',
    width: '0%',
    height: '1px',
    background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent)',
    transition: 'width 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  },
  inputUnderlineActive: {
    width: '100%',
  },
  inputGlow: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'radial-gradient(circle at center, rgba(255, 255, 255, 0.03) 0%, transparent 70%)',
    pointerEvents: 'none',
    borderRadius: '12px',
  },
  button: {
    width: '100%',
    padding: '20px 24px',
    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    borderRadius: '12px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    marginTop: '12px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
    position: 'relative',
    overflow: 'hidden',
    letterSpacing: '0.5px',
  },
  buttonDisabled: {
    background: 'rgba(0, 0, 0, 0.3)',
    cursor: 'not-allowed',
    boxShadow: 'none',
    opacity: 0.5,
    borderColor: 'rgba(255, 255, 255, 0.05)',
  },
  buttonSpinner: {
    width: '16px',
    height: '16px',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    borderTopColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    display: 'inline-block',
  },
  successMessage: {
    marginTop: '24px',
    padding: '16px 20px',
    background: 'rgba(16, 185, 129, 0.1)',
    border: '1px solid rgba(16, 185, 129, 0.2)',
    borderRadius: '12px',
    color: '#10b981',
    textAlign: 'center',
    fontSize: '14px',
    fontWeight: '500',
    animation: 'slideIn 0.3s ease',
    letterSpacing: '0.3px',
  },
  errorMessage: {
    marginTop: '24px',
    padding: '16px 20px',
    background: 'rgba(239, 68, 68, 0.1)',
    border: '1px solid rgba(239, 68, 68, 0.2)',
    borderRadius: '12px',
    color: '#ef4444',
    textAlign: 'center',
    fontSize: '14px',
    fontWeight: '500',
    animation: 'slideIn 0.3s ease',
    letterSpacing: '0.3px',
  },
};
