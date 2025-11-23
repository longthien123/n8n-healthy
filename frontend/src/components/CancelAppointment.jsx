import React, { useState, useEffect } from 'react';
import axios from '../utils/AxiosCustom';

const CancelAppointment = () => {
  const [appointmentId, setAppointmentId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState('');
  const [countdown, setCountdown] = useState(null);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    if (id) {
      setAppointmentId(id);
    } else {
      setMessage('Không tìm thấy ID lịch hẹn');
      setStatus('error');
    }
  }, []);

  const handleCancel = async () => {
    if (!window.confirm('Bạn có chắc chắn muốn hủy lịch hẹn này?')) {
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`appointments/appointments/${appointmentId}/cancel-by-id/`);
      
      if (response.success) {
        setMessage(response.message);
        setStatus('success');
        
        // Bắt đầu countdown 3 giây
        setCountdown(3);
        
        const timer = setInterval(() => {
          setCountdown(prev => {
            if (prev <= 1) {
              clearInterval(timer);
              // Thử đóng tab
              if (window.opener) {
                window.close();
              } else {
                // Fallback: về trang chủ
                window.location.href = '/';
              }
              return 0;
            }
            return prev - 1;
          });
        }, 1000);
        
      } else {
        setMessage(response.message);
        setStatus('error');
      }
    } catch (error) {
      console.error('❌ Error:', error);
      
      let errorMessage = 'Có lỗi xảy ra khi hủy lịch hẹn';
      
      if (error.response?.status === 404) {
        errorMessage = 'Lịch hẹn không tồn tại';
      } else if (error.response?.status === 500) {
        errorMessage = 'Lỗi server';
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      }
      
      setMessage(errorMessage);
      setStatus('error');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (window.opener) {
      window.close();
    } else {
      window.location.href = '/';
    }
  };

  return (
    <div style={{ 
      padding: 40, 
      fontFamily: 'sans-serif', 
      maxWidth: 500, 
      margin: '50px auto',
      textAlign: 'center',
      border: '1px solid #ddd',
      borderRadius: 8,
      backgroundColor: '#f9f9f9'
    }}>
      <h2 style={{ color: '#333', marginBottom: 20 }}>
        Hủy lịch hẹn
      </h2>
      
      {appointmentId && !message && (
        <>
          <p style={{ marginBottom: 30, fontSize: 16 }}>
            Bạn có chắc chắn muốn hủy lịch hẹn không?
          </p>
          
          <div style={{ display: 'flex', gap: 15, justifyContent: 'center' }}>
            <button 
              onClick={handleCancel}
              disabled={loading}
              style={{
                backgroundColor: loading ? '#ccc' : '#dc3545',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: 5,
                fontSize: 16,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? 'Đang hủy...' : 'Xác nhận hủy'}
            </button>
            
            <button 
              onClick={handleClose}
              disabled={loading}
              style={{
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: 5,
                fontSize: 16,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              Đóng
            </button>
          </div>
        </>
      )}

      {message && (
        <div style={{
          padding: 15,
          marginTop: 20,
          borderRadius: 5,
          backgroundColor: status === 'success' ? '#d4edda' : '#f8d7da',
          color: status === 'success' ? '#155724' : '#721c24',
          border: `1px solid ${status === 'success' ? '#c3e6cb' : '#f5c6cb'}`
        }}>
          <div style={{ fontSize: 16, marginBottom: 10 }}>
            {status === 'success' ? '✅' : '❌'} {message}
          </div>
          
          {status === 'success' && countdown !== null && (
            <>
              <div style={{ 
                fontSize: 18, 
                fontWeight: 'bold', 
                marginBottom: 15,
                color: '#155724' 
              }}>
                Đóng sau: {countdown} giây
              </div>
              
              <button 
                onClick={handleClose}
                style={{
                  backgroundColor: '#28a745',
                  color: 'white',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: 4,
                  fontSize: 14,
                  cursor: 'pointer'
                }}
              >
                Đóng ngay
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default CancelAppointment;