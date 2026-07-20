import { useEffect, useState } from 'react';
import ApprovalCard from '../components/ApprovalCard';

// This would come from an environment variable in a real app
const API_URL = import.meta.env.VITE_SUPPORT_API_URL || 'http://localhost:8000/api/v1';

const Dashboard = () => {
  const [approvals, setApprovals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchApprovals = async () => {
    try {
      const res = await fetch(`${API_URL}/approvals/pending`);
      const data = await res.json();
      setApprovals(data.approvals || []);
    } catch (error) {
      console.error("Failed to fetch approvals:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApprovals();
    // Poll every 5 seconds for new approvals
    const interval = setInterval(fetchApprovals, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleDecision = async (threadId: string, approved: boolean, comment: string) => {
    try {
      await fetch(`${API_URL}/approvals/${threadId}/decision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approved,
          reviewer_comment: comment
        })
      });
      // Refresh list immediately
      fetchApprovals();
    } catch (error) {
      console.error("Failed to submit decision:", error);
      alert("Error submitting decision");
    }
  };

  return (
    <div>
      <h1>Pending Approvals</h1>
      <p className="page-description">
        Review and approve sensitive actions proposed by the AI agents.
      </p>

      {loading && approvals.length === 0 ? (
        <div>Loading...</div>
      ) : approvals.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          No pending approvals requiring your attention.
        </div>
      ) : (
        <div className="grid">
          {approvals.map((req) => (
            <ApprovalCard 
              key={req.approval_id} 
              request={req} 
              onDecision={handleDecision} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
