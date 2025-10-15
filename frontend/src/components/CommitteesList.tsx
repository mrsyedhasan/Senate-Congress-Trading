import React, { useState, useEffect } from 'react';
import { Table, Card, Select, Button, Space, Tag, Spin, Alert, Statistic, Row, Col, Collapse } from 'antd';
import { ReloadOutlined, BankOutlined, TeamOutlined } from '@ant-design/icons';
import { getCommittees, type Committee as APICommittee } from '../services/api';
import type { ColumnsType } from 'antd/es/table';

const { Option } = Select;
const { Panel } = Collapse;

interface Committee {
  id: number;
  name: string;
  code: string;
  chamber: string;
  subcommittee: boolean;
  parent_committee_id?: number;
  description?: string;
  created_at: string;
  updated_at: string;
}

const CommitteesList: React.FC = () => {
  const [committees, setCommittees] = useState<Committee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    chamber: '',
    subcommittee: '',
  });

  useEffect(() => {
    fetchCommittees();
  }, []);

  const fetchCommittees = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      if (filters.chamber) params.append('chamber', filters.chamber);
      if (filters.subcommittee !== '') params.append('subcommittee', filters.subcommittee);

      const data = await getCommittees(params.toString());
      setCommittees(data as Committee[]);
    } catch (err) {
      setError('Failed to load committees');
      console.error('Error fetching committees:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleSearch = () => {
    fetchCommittees();
  };

  const handleReset = () => {
    setFilters({
      chamber: '',
      subcommittee: '',
    });
    fetchCommittees();
  };

  const getChamberColor = (chamber: string) => {
    switch (chamber?.toLowerCase()) {
      case 'house': return 'green';
      case 'senate': return 'purple';
      case 'joint': return 'orange';
      default: return 'default';
    }
  };

  const getTypeColor = (isSubcommittee: boolean) => {
    return isSubcommittee ? 'blue' : 'gold';
  };

  const columns: ColumnsType<Committee> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: Committee) => (
        <div>
          <div style={{ fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
            <BankOutlined style={{ marginRight: 8, color: '#1890ff' }} />
            {name}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            Code: {record.code}
          </div>
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
        { text: 'Joint', value: 'Joint' },
      ],
      onFilter: (value, record) => record.chamber === value,
    },
    {
      title: 'Type',
      dataIndex: 'subcommittee',
      key: 'subcommittee',
      render: (isSubcommittee: boolean) => (
        <Tag color={getTypeColor(isSubcommittee)}>
          {isSubcommittee ? 'Subcommittee' : 'Committee'}
        </Tag>
      ),
      filters: [
        { text: 'Committee', value: false },
        { text: 'Subcommittee', value: true },
      ],
      onFilter: (value, record) => record.subcommittee === value,
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      render: (description: string) => (
        <div style={{ maxWidth: 300 }}>
          {description ? (
            description.length > 100 ? (
              <span>
                {description.substring(0, 100)}...
              </span>
            ) : (
              description
            )
          ) : (
            'N/A'
          )}
        </div>
      ),
    },
  ];

  // Calculate statistics
  const totalCommittees = committees.length;
  const mainCommittees = committees.filter(c => !c.subcommittee).length;
  const subcommittees = committees.filter(c => c.subcommittee).length;
  const houseCommittees = committees.filter(c => c.chamber === 'House').length;
  const senateCommittees = committees.filter(c => c.chamber === 'Senate').length;
  const jointCommittees = committees.filter(c => c.chamber === 'Joint').length;

  // Group committees by chamber and type
  const groupedCommittees = committees.reduce((acc, committee) => {
    const key = `${committee.chamber}-${committee.subcommittee ? 'sub' : 'main'}`;
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(committee);
    return acc;
  }, {} as Record<string, Committee[]>);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <p>Loading committees...</p>
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
      <h1>Congressional Committees</h1>
      
      {/* Statistics */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Total Committees"
              value={totalCommittees}
              prefix={<BankOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Main Committees"
              value={mainCommittees}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Subcommittees"
              value={subcommittees}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Chambers"
              value={`${houseCommittees}H, ${senateCommittees}S, ${jointCommittees}J`}
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
              <Option value="Joint">Joint</Option>
            </Select>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Select
              placeholder="Committee Type"
              value={filters.subcommittee}
              onChange={(value) => handleFilterChange('subcommittee', value)}
              style={{ width: '100%' }}
              allowClear
            >
              <Option value="false">Main Committee</Option>
              <Option value="true">Subcommittee</Option>
            </Select>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Space>
              <Button type="primary" onClick={handleSearch}>
                Search
              </Button>
              <Button onClick={handleReset} icon={<ReloadOutlined />}>
                Reset
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Grouped View */}
      <Card title="Committee Overview" style={{ marginBottom: 16 }}>
        <Collapse>
          {Object.entries(groupedCommittees).map(([groupKey, groupCommittees]) => {
            const [chamber, type] = groupKey.split('-');
            return (
              <Panel 
                header={`${chamber} ${type === 'main' ? 'Committees' : 'Subcommittees'} (${groupCommittees.length})`}
                key={groupKey}
              >
                <Row gutter={[16, 16]}>
                  {groupCommittees.map(committee => (
                    <Col xs={24} sm={12} md={8} lg={6} key={committee.id}>
                      <Card size="small" style={{ height: '100%' }}>
                        <div style={{ fontWeight: 'bold', marginBottom: 8 }}>
                          {committee.name}
                        </div>
                        <div style={{ fontSize: '12px', color: '#666', marginBottom: 8 }}>
                          Code: {committee.code}
                        </div>
                        <div style={{ fontSize: '12px', color: '#666' }}>
                          {committee.description ? (
                            committee.description.length > 80 ? (
                              `${committee.description.substring(0, 80)}...`
                            ) : (
                              committee.description
                            )
                          ) : (
                            'No description available'
                          )}
                        </div>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Panel>
            );
          })}
        </Collapse>
      </Card>

      {/* Committees Table */}
      <Card className="table-container">
        <Table
          columns={columns}
          dataSource={committees}
          rowKey="id"
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} of ${total} committees`,
          }}
          scroll={{ x: 800 }}
        />
      </Card>
    </div>
  );
};

export default CommitteesList;
