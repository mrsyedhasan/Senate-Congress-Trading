import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Dashboard from './components/Dashboard';
import TradesList from './components/TradesList';
import MembersList from './components/MembersList';
import CommitteesList from './components/CommitteesList';
import Navbar from './components/Navbar';
import './App.css';

const { Content } = Layout;

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Navbar />
        <Content style={{ padding: '24px' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/trades" element={<TradesList />} />
            <Route path="/members" element={<MembersList />} />
            <Route path="/committees" element={<CommitteesList />} />
          </Routes>
        </Content>
      </Layout>
    </Router>
  );
}

export default App;
