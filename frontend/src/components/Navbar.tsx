import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  SwapOutlined,
  TeamOutlined,
  BankOutlined
} from '@ant-design/icons';

const { Header } = Layout;
const { Title } = Typography;

const Navbar: React.FC = () => {
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: <Link to="/">Dashboard</Link>,
    },
    {
      key: '/trades',
      icon: <SwapOutlined />,
      label: <Link to="/trades">Trades</Link>,
    },
    {
      key: '/members',
      icon: <TeamOutlined />,
      label: <Link to="/members">Members</Link>,
    },
    {
      key: '/committees',
      icon: <BankOutlined />,
      label: <Link to="/committees">Committees</Link>,
    },
  ];

  return (
    <Header style={{ 
      display: 'flex', 
      alignItems: 'center', 
      background: '#fff',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      padding: '0 24px'
    }}>
      <Title level={3} style={{ margin: 0, marginRight: 32, color: '#1890ff' }}>
        🏛️ Congressional Trading Dashboard
      </Title>
      <Menu
        theme="light"
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        style={{ flex: 1, borderBottom: 'none' }}
      />
    </Header>
  );
};

export default Navbar;
