import React, { useState, useEffect } from 'react';
import { Table, Card, Select, Input, DatePicker, Button, Space, Tag, Spin, Alert, Row, Col } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import { getTrades, type Trade } from '../services/api';
import type { ColumnsType } from 'antd/es/table';

const { Option } = Select;
const { RangePicker } = DatePicker;

const TradesList: React.FC = () => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    chamber: '',
    party: '',
    ticker: '',
    transaction_type: '',
    dateRange: null as any,
  });

  useEffect(() => {
    fetchTrades();
  }, []);

  const fetchTrades = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      // Set limit to get all trades (backend default is 100, we have 400+)
      params.append('limit', '1000');
      
      if (filters.chamber) params.append('chamber', filters.chamber);
      if (filters.party) params.append('party', filters.party);
      if (filters.ticker) params.append('ticker', filters.ticker);
      if (filters.transaction_type) params.append('transaction_type', filters.transaction_type);
      if (filters.dateRange) {
        params.append('start_date', filters.dateRange[0].format('YYYY-MM-DD'));
        params.append('end_date', filters.dateRange[1].format('YYYY-MM-DD'));
      }

      const data = await getTrades(params.toString());
      setTrades(data);
    } catch (err) {
      setError('Failed to load trades');
      console.error('Error fetching trades:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleSearch = () => {
    fetchTrades();
  };

  const handleReset = () => {
    setFilters({
      chamber: '',
      party: '',
      ticker: '',
      transaction_type: '',
      dateRange: null,
    });
    fetchTrades();
  };

  const formatAmount = (trade: Trade) => {
    // For Exchange transactions, show both FROM and TO amounts
    if (trade.transaction_type === 'Exchange' && trade.exchange_from_amount) {
      const fromAmount = trade.exchange_from_amount.toLocaleString();
      const toAmount = trade.amount_exact ? 
        trade.amount_exact.toLocaleString() : 
        (trade.amount_min ? trade.amount_min.toLocaleString() : 'N/A');
      
      return (
        <div>
          <div style={{ color: '#ff4d4f' }}>FROM: ${fromAmount}</div>
          <div style={{ color: '#52c41a' }}>TO: ${toAmount}</div>
          {trade.exchange_ratio && (
            <div style={{ fontSize: '11px', color: '#666' }}>
              Ratio: {trade.exchange_ratio}:1
            </div>
          )}
        </div>
      );
    }
    
    // Regular Buy/Sell transactions
    if (trade.amount_exact) {
      return `$${trade.amount_exact.toLocaleString()}`;
    } else if (trade.amount_min && trade.amount_max) {
      return `$${trade.amount_min.toLocaleString()} - $${trade.amount_max.toLocaleString()}`;
    } else if (trade.amount_min) {
      return `$${trade.amount_min.toLocaleString()}+`;
    } else {
      return 'N/A';
    }
  };

  const getTransactionTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'buy': return 'green';
      case 'sell': return 'red';
      case 'exchange': return 'blue';
      default: return 'default';
    }
  };

  const getPartyColor = (party: string) => {
    switch (party.toLowerCase()) {
      case 'republican': return 'red';
      case 'democrat': return 'blue';
      case 'independent': return 'orange';
      default: return 'default';
    }
  };


  const columns: ColumnsType<Trade> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
      render: (id: number) => (
        <div style={{ fontSize: '11px', color: '#999' }}>
          #{id}
        </div>
      ),
    },
    {
      title: 'Member',
      dataIndex: 'member',
      key: 'member',
      render: (member: Trade['member']) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{member.name}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {member.chamber} • {member.state}
          </div>
        </div>
      ),
      sorter: (a, b) => a.member.name.localeCompare(b.member.name),
    },
    {
      title: 'Party',
      dataIndex: ['member', 'party'],
      key: 'party',
      render: (party: string) => (
        <Tag color={getPartyColor(party)}>{party}</Tag>
      ),
      filters: [
        { text: 'Republican', value: 'Republican' },
        { text: 'Democrat', value: 'Democrat' },
        { text: 'Independent', value: 'Independent' },
      ],
      onFilter: (value, record) => record.member.party === value,
    },
    {
      title: 'Stock',
      dataIndex: 'ticker',
      key: 'ticker',
      render: (ticker: string, record: Trade) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{ticker}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {record.company_name}
          </div>
        </div>
      ),
    },
    {
      title: 'Type',
      dataIndex: 'transaction_type',
      key: 'transaction_type',
      render: (type: string, record: Trade) => (
        <div>
          <Tag color={getTransactionTypeColor(type)}>{type}</Tag>
          {type === 'Exchange' && record.exchange_from_ticker && (
            <div style={{ fontSize: '11px', color: '#666', marginTop: '2px' }}>
              FROM: {record.exchange_from_ticker} → TO: {record.ticker}
              {record.exchange_reason && (
                <div style={{ fontStyle: 'italic' }}>
                  Reason: {record.exchange_reason}
                </div>
              )}
            </div>
          )}
        </div>
      ),
      filters: [
        { text: 'Buy', value: 'Buy' },
        { text: 'Sell', value: 'Sell' },
        { text: 'Exchange', value: 'Exchange' },
      ],
      onFilter: (value, record) => record.transaction_type === value,
    },
    {
      title: 'Committee',
      key: 'committee',
      render: (_, record: Trade) => {
        const committees = record.member.committees || [];
        if (committees.length === 0) {
          return <span style={{ color: '#999', fontSize: '12px' }}>No committees</span>;
        }
        
        // Show first 2 committees, with "..." if more
        const displayCommittees = committees.slice(0, 2);
        const hasMore = committees.length > 2;
        
        return (
          <div>
            {displayCommittees.map((committee, index) => (
              <div key={committee.id} style={{ fontSize: '11px', marginBottom: '2px' }}>
                <Tag color="blue" style={{ fontSize: '10px' }}>
                  {committee.name.length > 25 ? 
                    committee.name.substring(0, 25) + '...' : 
                    committee.name
                  }
                </Tag>
              </div>
            ))}
            {hasMore && (
              <div style={{ fontSize: '10px', color: '#666', fontStyle: 'italic' }}>
                +{committees.length - 2} more
              </div>
            )}
          </div>
        );
      },
    },
    {
      title: 'Amount',
      key: 'amount',
      render: (_, record) => formatAmount(record),
      sorter: (a, b) => {
        const amountA = a.amount_exact || a.amount_min || 0;
        const amountB = b.amount_exact || b.amount_min || 0;
        return amountA - amountB;
      },
    },
    {
      title: 'Trade Date',
      dataIndex: 'transaction_date',
      key: 'transaction_date',
      render: (date: string) => {
        const d = new Date(date);
        const estTime = d.toLocaleString('en-US', {
          timeZone: 'America/New_York',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        });
        
        const [datePart, timePart] = estTime.split(', ');
        const [time, ampm] = timePart.split(' ');
        
        return (
          <div>
            <div>{datePart}</div>
            <div style={{ fontSize: '11px', color: '#999' }}>
              {time} {ampm} EST
            </div>
          </div>
        );
      },
      sorter: (a, b) => new Date(a.transaction_date).getTime() - new Date(b.transaction_date).getTime(),
      defaultSortOrder: 'descend',
    },
  ];

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <p>Loading trades...</p>
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
      <h1>Congressional Trades</h1>
      
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
              placeholder="Stock Ticker"
              value={filters.ticker}
              onChange={(e) => handleFilterChange('ticker', e.target.value)}
              prefix={<SearchOutlined />}
            />
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Select
              placeholder="Transaction Type"
              value={filters.transaction_type}
              onChange={(value) => handleFilterChange('transaction_type', value)}
              style={{ width: '100%' }}
              allowClear
            >
              <Option value="Buy">Buy</Option>
              <Option value="Sell">Sell</Option>
              <Option value="Exchange">Exchange</Option>
            </Select>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <RangePicker
              value={filters.dateRange}
              onChange={(dates) => handleFilterChange('dateRange', dates)}
              style={{ width: '100%' }}
            />
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

      {/* Trades Table */}
      <Card className="table-container">
        <Table
          columns={columns}
          dataSource={trades}
          rowKey="id"
          pagination={{
            pageSize: 20,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) =>
              `${range[0]}-${range[1]} of ${total} trades`,
          }}
          scroll={{ x: 800 }}
        />
      </Card>
    </div>
  );
};

export default TradesList;
