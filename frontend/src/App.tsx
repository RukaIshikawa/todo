import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Signup from './Signup';
import Login from './Login'; // ログイン画面があると仮定

const App = () => {
  return (
    <BrowserRouter>
      {/* ナビゲーションメニュー（リンク） */}
      <nav>
        <Link to="/signup">サインアップへ</Link> | 
        <Link to="/login">ログインへ</Link>
      </nav>

      {/* URLに応じて切り替わるエリア */}
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<h1>ホーム画面</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;