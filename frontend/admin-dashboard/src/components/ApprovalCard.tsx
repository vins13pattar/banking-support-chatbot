import React, { useState } from 'react';

interface ApprovalRequest {
  approval_id: string;
  thread_id: string;
  customer_id: string;
  action_type: string;
  action_summary: string;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  proposed_payload: any;
  requested_at: string;
}

interface Props {
  request: ApprovalRequest;
  onDecision: (threadId: string, approved: boolean, comment: string) => Promise<void>;
}

const ApprovalCard: React.FC<Props> = ({ request, onDecision }) => {
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleDecision = async (approved: boolean) => {
    setIsSubmitting(true);
    try {
      await onDecision(request.thread_id, approved, comment);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <div className="card-title">{request.action_type}</div>
          <div className="card-subtitle">{new Date(request.requested_at).toLocaleString()}</div>
        </div>
        <span className={`badge ${request.risk_level}`}>
          {request.risk_level} Risk
        </span>
      </div>
      
      <div className="card-body">
        <div className="data-label">Summary</div>
        <div className="data-value">{request.action_summary}</div>
        
        <div className="data-label">Customer ID</div>
        <div className="data-value">{request.customer_id}</div>
        
        <div className="data-label">Payload</div>
        <div className="payload-box">
          {JSON.stringify(request.proposed_payload, null, 2)}
        </div>
      </div>
      
      <div style={{ marginBottom: '1rem' }}>
        <input 
          type="text" 
          placeholder="Reviewer comment (optional)" 
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          style={{ 
            width: '100%', 
            padding: '0.5rem', 
            borderRadius: '0.375rem',
            border: '1px solid var(--panel-border)',
            background: 'var(--bg-color)',
            color: 'white',
            outline: 'none'
          }}
        />
      </div>
      
      <div className="card-footer">
        <button 
          className="btn btn-danger" 
          onClick={() => handleDecision(false)}
          disabled={isSubmitting}
        >
          Reject
        </button>
        <button 
          className="btn btn-primary" 
          onClick={() => handleDecision(true)}
          disabled={isSubmitting}
        >
          Approve
        </button>
      </div>
    </div>
  );
};

export default ApprovalCard;
