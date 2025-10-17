import React, { useState, useEffect } from 'react';
import { Table, Card, Select, Input, Button, Space, Tag, Spin, Alert, Statistic, Row, Col } from 'antd';
import { SearchOutlined, ReloadOutlined, UserOutlined } from '@ant-design/icons';
import { getMembers, type Member } from '../services/api';
import type { ColumnsType } from 'antd/es/table';

const { Option } = Select;

const MembersList: React.FC = () => {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    chamber: '',
    party: '',
    state: '',
    has_trades: '',
  });

  useEffect(() => {
    fetchMembers();
  }, []);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      // Set limit to get all members (backend default is 100, we have 145)
      params.append('limit', '1000');
      
      if (filters.chamber) params.append('chamber', filters.chamber);
      if (filters.party) params.append('party', filters.party);
      if (filters.state) params.append('state', filters.state);
      if (filters.has_trades !== '') params.append('has_trades', filters.has_trades);

      const data = await getMembers(params.toString());
      setMembers(data);
    } catch (err) {
      setError('Failed to load members');
      console.error('Error fetching members:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleSearch = () => {
    fetchMembers();
  };

  const handleReset = () => {
    setFilters({
      chamber: '',
      party: '',
      state: '',
      has_trades: '',
    });
    fetchMembers();
  };

  const getPartyColor = (party: string) => {
    switch (party?.toLowerCase()) {
      case 'republican': return 'red';
      case 'democrat': return 'blue';
      case 'independent': return 'orange';
      default: return 'default';
    }
  };

  const getChamberColor = (chamber: string) => {
    switch (chamber?.toLowerCase()) {
      case 'house': return 'green';
      case 'senate': return 'purple';
      default: return 'default';
    }
  };

  const columns: ColumnsType<Member> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: Member) => (
        <div>
          <div style={{ fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
            <UserOutlined style={{ marginRight: 8, color: '#1890ff' }} />
            {name}
          </div>
          {record.district && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              District {record.district}
            </div>
          )}
        </div>
      ),
      sorter: (a, b) => a.name.localeCompare(b.name),
    },
    {
      title: 'Chamber',
      dataIndex: 'chamber',
      key: 'chamber',
      render: (chamber: string) => (
        <Tag color={getChamberColor(chamber)}>{chamber}</Tag>
      ),
      filters: [
        { text: 'House', value: 'House' },
        { text: 'Senate', value: 'Senate' },
      ],
      onFilter: (value, record) => record.chamber === value,
    },
    {
      title: 'State',
      dataIndex: 'state',
      key: 'state',
      sorter: (a, b) => a.state.localeCompare(b.state),
    },
    {
      title: 'Party',
      dataIndex: 'party',
      key: 'party',
      render: (party: string) => (
        <Tag color={getPartyColor(party)}>{party}</Tag>
      ),
      filters: [
        { text: 'Republican', value: 'Republican' },
        { text: 'Democrat', value: 'Democrat' },
        { text: 'Independent', value: 'Independent' },
      ],
      onFilter: (value, record) => record.party === value,
    },
    {
      title: 'Contact',
      key: 'contact',
      render: (_, record: Member) => (
        <div>
          {record.phone && (
            <div style={{ fontSize: '12px' }}>📞 {record.phone}</div>
          )}
          {record.email && (
            <div style={{ fontSize: '12px' }}>✉️ {record.email}</div>
          )}
          {record.website && (
            <div style={{ fontSize: '12px' }}>
              🌐 <a href={record.website} target="_blank" rel="noopener noreferrer">
                Website
              </a>
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Office',
      dataIndex: 'office',
      key: 'office',
      render: (office: string) => office || 'N/A',
    },
  ];

  // Calculate statistics
  const totalMembers = members.length;
  const houseMembers = members.filter(m => m.chamber === 'House').length;
  const senateMembers = members.filter(m => m.chamber === 'Senate').length;
  const republicans = members.filter(m => m.party === 'Republican').length;
  const democrats = members.filter(m => m.party === 'Democrat').length;
  const independents = members.filter(m => m.party === 'Independent').length;

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <p>Loading members...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error"
        description={error}
        type="error"
        showIcon
        style={{ margin: '20px 0' }}
      />
    );
  }

  return (
    <div>
      <h1>Congressional Members</h1>
      
      {/* Statistics */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Total Members"
              value={totalMembers}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="House Members"
              value={houseMembers}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Senate Members"
              value={senateMembers}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Parties"
              value={`${republicans}R, ${democrats}D, ${independents}I`}
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Filters */}
      <Card className="filter-section">
        <Row gutter={[16, 16]} align="middle">
          <Col xs={24} sm={12} md={6}>
            <Select
              placeholder="Chamber"
              value={filters.chamber}
              onChange={(value) => handleFilterChange('chamber', value)}
              style={{ width: '100%' }}
              allowClear
            >
              <Option value="House">House</Option>
              <Option value="Senate">Senate</Option>
            </Select>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Select
              placeholder="Party"
              value={filters.party}
              onChange={(value) => handleFilterChange('party', value)}
              style={{ width: '100%' }}
              allowClear
            >
              <Option value="Republican">Republican</Option>
              <Option value="Democrat">Democrat</Option>
              <Option value="Independent">Independent</Option>
            </Select>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Input
              placeholder="State"
              value={filters.state}
              onChange={(e) => handleFilterChange('state', e.target.value)}
              prefix={<SearchOutlined />}
            />
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Select
              placeholder="Has Trades"
              value={filters.has_trades}
              onChange={(value) => handleFilterChange('has_trades', value)}
              style={{ width: '100%' }}
              allowClear
            >
              <Option value="true">Yes</Option>
              <Option value="false">No</Option>
            </Select>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Space>
              <Button type="primary" onClick={handleSearch} icon={<SearchOutlined />}>
                Search
              </Button>
              <Button onClick={handleReset} icon={<ReloadOutlined />}>
                Reset
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Members Table */}
      <Card className="table-container">
        <Table
          columns={columns}
          dataSource={members}
          rowKey="id"
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} of ${total} members`,
          }}
          scroll={{ x: 800 }}
        />
      </Card>
    </div>
  );
};

export default MembersList;
