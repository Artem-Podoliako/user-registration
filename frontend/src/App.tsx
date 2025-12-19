import RegisterForm from './RegisterForm';

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      width: '100%',
      margin: 0,
      padding: 0,
      background: 'linear-gradient(135deg, #000000 0%, #0a0a0f 25%, #0d0d14 50%, #0a0a0f 75%, #000000 100%)',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* Темные декоративные элементы */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: `
          radial-gradient(circle at 15% 30%, rgba(30, 30, 50, 0.4) 0%, transparent 60%),
          radial-gradient(circle at 85% 70%, rgba(20, 20, 40, 0.3) 0%, transparent 60%),
          radial-gradient(circle at 50% 50%, rgba(15, 15, 30, 0.2) 0%, transparent 70%)
        `,
        animation: 'pulse 20s ease-in-out infinite',
      }} />
      
      {/* Тонкие линии для глубины */}
      <div style={{
        position: 'absolute',
        top: '20%',
        left: '10%',
        width: '1px',
        height: '200px',
        background: 'linear-gradient(to bottom, transparent, rgba(100, 100, 120, 0.1), transparent)',
        animation: 'fadeInOut 8s ease-in-out infinite',
      }} />
      <div style={{
        position: 'absolute',
        bottom: '15%',
        right: '15%',
        width: '150px',
        height: '1px',
        background: 'linear-gradient(to right, transparent, rgba(100, 100, 120, 0.1), transparent)',
        animation: 'fadeInOut 10s ease-in-out infinite',
      }} />
      
      <RegisterForm />
    </div>
  );
}

export default App;
