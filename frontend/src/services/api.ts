import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Types
export interface Trade {
  id: number;
  ticker: string;
  company_name?: string;
  transaction_type: string;
  transaction_date: string;
  amount_min?: number;
  amount_max?: number;
  amount_exact?: number;
  // Exchange-specific fields
  exchange_from_ticker?: string;
  exchange_from_company?: string;
  exchange_from_amount?: number;
  exchange_ratio?: number;
  exchange_reason?: string;
  description?: string;
  source?: string;
  filing_date?: string;
  member: {
    id: number;
    name: string;
    chamber: string;
    party: string;
    state: string;
    district?: string;
  };
}

export interface Member {
  id: number;
  name: string;
  chamber: string;
  state: string;
  party: string;
  district?: string;
  office?: string;
  phone?: string;
  email?: string;
  website?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

export interface Committee {
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

export interface DashboardStats {
  total_trades: number;
  total_members: number;
  total_committees: number;
  recent_trades_count: number;
  top_traded_stocks: Array<{
    ticker: string;
    trade_count: number;
  }>;
  trades_by_chamber: {[key: string]: number};
  trades_by_party: {[key: string]: number};
}

// API Functions
export const getDashboardStats = async (): Promise<DashboardStats> => {
  const response = await api.get('/api/trades/stats');
  return response.data;
};

export const getTrades = async (params?: string): Promise<Trade[]> => {
  const url = params ? `/api/trades?${params}` : '/api/trades';
  const response = await api.get(url);
  return response.data;
};

export const getRecentTrades = async (days: number = 30, limit: number = 50): Promise<Trade[]> => {
  const response = await api.get(`/api/trades/recent?days=${days}&limit=${limit}`);
  return response.data;
};

export const getTradesByMember = async (memberId: number): Promise<Trade[]> => {
  const response = await api.get(`/api/trades/by-member/${memberId}`);
  return response.data;
};

export const getTradesByTicker = async (ticker: string): Promise<Trade[]> => {
  const response = await api.get(`/api/trades/by-ticker/${ticker}`);
  return response.data;
};

export const getTrade = async (tradeId: number): Promise<Trade> => {
  const response = await api.get(`/api/trades/${tradeId}`);
  return response.data;
};

export const getMembers = async (params?: string): Promise<Member[]> => {
  const url = params ? `/api/members?${params}` : '/api/members';
  const response = await api.get(url);
  return response.data;
};

export const getMembersByChamber = async (chamber: string): Promise<Member[]> => {
  const response = await api.get(`/api/members/by-chamber/${chamber}`);
  return response.data;
};

export const getMembersByState = async (state: string): Promise<Member[]> => {
  const response = await api.get(`/api/members/by-state/${state}`);
  return response.data;
};

export const getMembersByParty = async (party: string): Promise<Member[]> => {
  const response = await api.get(`/api/members/by-party/${party}`);
  return response.data;
};

export const getMostActiveTraders = async (limit: number = 10): Promise<Member[]> => {
  const response = await api.get(`/api/members/most-active?limit=${limit}`);
  return response.data;
};

export const getMember = async (memberId: number): Promise<Member> => {
  const response = await api.get(`/api/members/${memberId}`);
  return response.data;
};

export const searchMembers = async (name: string): Promise<Member[]> => {
  const response = await api.get(`/api/members/search/${name}`);
  return response.data;
};

export const getCommittees = async (params?: string): Promise<Committee[]> => {
  const url = params ? `/api/committees?${params}` : '/api/committees';
  const response = await api.get(url);
  return response.data;
};

export const getCommitteesByChamber = async (chamber: string): Promise<Committee[]> => {
  const response = await api.get(`/api/committees/by-chamber/${chamber}`);
  return response.data;
};

export const getMainCommittees = async (chamber?: string): Promise<Committee[]> => {
  const params = chamber ? `?chamber=${chamber}` : '';
  const response = await api.get(`/api/committees/main${params}`);
  return response.data;
};

export const getSubcommittees = async (parentCommitteeId?: number): Promise<Committee[]> => {
  const params = parentCommitteeId ? `?parent_committee_id=${parentCommitteeId}` : '';
  const response = await api.get(`/api/committees/subcommittees${params}`);
  return response.data;
};

export const getCommittee = async (committeeId: number): Promise<Committee> => {
  const response = await api.get(`/api/committees/${committeeId}`);
  return response.data;
};

export const getCommitteeMembers = async (committeeId: number): Promise<Member[]> => {
  const response = await api.get(`/api/committees/${committeeId}/members`);
  return response.data;
};

export const getMemberCommittees = async (memberId: number): Promise<Committee[]> => {
  const response = await api.get(`/api/committees/member/${memberId}/committees`);
  return response.data;
};

export const collectData = async (): Promise<{message: string}> => {
  const response = await api.post('/api/collect-data');
  return response.data;
};

export const healthCheck = async (): Promise<{status: string; timestamp: string}> => {
  const response = await api.get('/api/health');
  return response.data;
};

export default api;
