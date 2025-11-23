import React, { useState, useEffect } from 'react';

const ActivationResult = () => {
  const [countdown, setCountdown] = useState(3);
  const [status, setStatus] = useState('');

  useEffect(() => {
    // Lấy status từ URL
    const urlParams = new URLSearchParams(window.location.search);
    const activationStatus = urlParams.get('status');
    setStatus(activationStatus);

    // Bắt đầu countdown
    if (activationStatus === 'success') {
      const timer = setInterval(() => {
        setCountdown(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            // Chuyển hướng đến trang đăng nhập
            window.location.href = '/login';
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      // Cleanup timer khi component unmount
      return () => clearInterval(timer);
    }
  }, []);

  const handleGoToLogin = () => {
    window.location.href = '/login';
  };

  return (
    <div style={{ 
      padding: 40, 
      fontFamily: 'sans-serif', 
      maxWidth: 500, 
      margin: '100px auto',
      textAlign: 'center',
      border: '1px solid #ddd',
      borderRadius: 8,
      backgroundColor: '#f9f9f9'
    }}>
      {status === 'success' ? (
        <>
          <div style={{ fontSize: 48, marginBottom: 20 }}>✅</div>
          <h2 style={{ color: '#28a745', marginBottom: 20 }}>
            Kích hoạt tài khoản thành công!
          </h2>
          <p style={{ fontSize: 16, marginBottom: 30, color: '#6c757d' }}>
            Tài khoản của bạn đã được kích hoạt thành công.<br/>
            Bạn có thể đăng nhập ngay bây giờ.
          </p>
          
          <div style={{ 
            fontSize: 18, 
            fontWeight: 'bold', 
            marginBottom: 20,
            color: '#28a745'
          }}>
            Chuyển đến trang đăng nhập sau: {countdown} giây
          </div>
          
          <button 
            onClick={handleGoToLogin}
            style={{
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              padding: '12px 24px',
              borderRadius: 5,
              fontSize: 16,
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#218838'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#28a745'}
          >
            Đăng nhập ngay
          </button>
        </>
      ) : status === 'error' ? (
        <>
          <div style={{ fontSize: 48, marginBottom: 20 }}>❌</div>
          <h2 style={{ color: '#dc3545', marginBottom: 20 }}>
            Kích hoạt tài khoản thất bại
          </h2>
          <p style={{ fontSize: 16, marginBottom: 30, color: '#6c757d' }}>
            Link kích hoạt không hợp lệ hoặc đã hết hạn.<br/>
            Vui lòng liên hệ bộ phận hỗ trợ hoặc đăng ký lại.
          </p>
          
          <div style={{ display: 'flex', gap: 15, justifyContent: 'center' }}>
            <button 
              onClick={() => window.location.href = '/info-patient'}
              style={{
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: 5,
                fontSize: 16,
                cursor: 'pointer'
              }}
            >
              Đăng ký lại
            </button>
            
            <button 
              onClick={handleGoToLogin}
              style={{
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: 5,
                fontSize: 16,
                cursor: 'pointer'
              }}
            >
              Trang đăng nhập
            </button>
          </div>
        </>
      ) : (
        <div>Đang xử lý...</div>
      )}
    </div>
  );
};

export default ActivationResult;