import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);

    try {
      const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: form.toString(),
    })

      const data = await response.json();
      

      if (response.ok) {
        // --- ここが重要！ ---
        // サーバーから届いたトークン（身分証）をブラウザの保存スペースに入れる
        localStorage.setItem('token', data.access_token);
            
        setMessage('ログイン成功！ホームへ移動します...');
            
        // 2秒後にマイページやホームへ飛ばす
        setTimeout(() => navigate('/dashboard'), 2000);
      } else {
        setMessage('ユーザー名またはパスワードが違います。');
      }
    } catch (error) {
        setMessage('サーバーに接続できません。');
    }
  };

  return (
    <div style={{ maxWidth: '300px', margin: '50px auto' }}>
      <h2>ログイン</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>ユーザー名:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: '100%', marginBottom: '10px' }}
            required
          />
        </div>
        <div>
          <label>パスワード:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', marginBottom: '10px' }}
            required
          />
        </div>
        <button type="submit" style={{ width: '100%' }}>ログイン</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Login;