import React from 'react';

interface Ticket {
  id: string;
  customer_id: string;
  thread_id: string;
  category: string;
  description: string;
  priority: string;
  status: string;
  assigned_to: string;
  created_at: string;
  updated_at: string;
}

interface Props {
  ticket: Ticket;
  onClose: () => void;
}

const TicketDetailModal: React.FC<Props> = ({ ticket, onClose }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div className="card-header">
          <div>
            <div className="card-title">{ticket.category}</div>
            <div className="card-subtitle">Ticket {ticket.id}</div>
          </div>
          <button className="modal-close" onClick={onClose} aria-label="Close">
            &times;
          </button>
        </div>

        <div className="card-body">
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem' }}>
            <span className={`badge ${ticket.status === 'open' ? 'warning' : 'low'}`}>
              {ticket.status}
            </span>
            <span className={`badge ${ticket.priority}`}>{ticket.priority}</span>
          </div>

          <div className="data-label">Description</div>
          <div className="data-value">{ticket.description || '—'}</div>

          <div className="data-label">Customer ID</div>
          <div className="data-value">{ticket.customer_id || '—'}</div>

          <div className="data-label">Thread ID</div>
          <div className="data-value">{ticket.thread_id}</div>

          <div className="data-label">Assigned To</div>
          <div className="data-value">{ticket.assigned_to || 'Unassigned'}</div>

          <div className="data-label">Created</div>
          <div className="data-value">{new Date(ticket.created_at).toLocaleString()}</div>

          <div className="data-label">Last Updated</div>
          <div className="data-value">{new Date(ticket.updated_at).toLocaleString()}</div>
        </div>
      </div>
    </div>
  );
};

export default TicketDetailModal;
