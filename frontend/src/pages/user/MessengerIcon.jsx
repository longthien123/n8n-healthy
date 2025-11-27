import React from 'react';

export default function MessengerIcon({
  size = 40,
  color = '#FFFFFF',
  bg = '#0084FF',
  className = '',
  ariaLabel = 'Messenger',
  onClick,
  showBadge = false,
  badgeCount = null,
}) {
  const sizeValue = typeof size === 'number' ? `${size}px` : size;

  const badgeContent = () => {
    if (!badgeCount && badgeCount !== 0) return '';
    if (typeof badgeCount === 'number' && badgeCount > 99) return '99+';
    return String(badgeCount);
  };

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={ariaLabel}
      title={ariaLabel}
      className={`inline-flex items-center justify-center rounded-full p-0 shadow-sm focus:outline-none ${className}`}
      style={{ width: sizeValue, height: sizeValue, background: 'transparent', border: 'none' }}
    >
      <div style={{ width: sizeValue, height: sizeValue, position: 'relative' }}>
        <svg
          viewBox="0 0 512 512"
          width={sizeValue}
          height={sizeValue}
          aria-hidden="true"
          focusable="false"
        >
          {/* nền tròn */}
          <circle cx="256" cy="256" r="256" fill={bg} />

          {/* logo Messenger */}
          <path
            fill={color}
            d="M256 88C153.8 88 72 163.1 72 256c0 52.4 
            25.8 98.8 66.2 129.7V424l63.5-34.9c17.1 4.7 
            35.4 7.3 54.3 7.3 102.2 0 184-75.1 
            184-168.4S358.2 88 256 88zm20.2 226.7l-46.9-50.1-91.5 
            50.1 101.1-107.3 49.9 50.1 88.5-50.1-101.1 
            107.3z"
          />
        </svg>

        {/* Badge thông báo */}
        {showBadge && (
          <div
            style={{
              position: 'absolute',
              top: -3,
              right: -3,
              minWidth: 18,
              height: 18,
              padding: '0 5px',
              borderRadius: 9,
              background: '#FF3B30',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 10,
              fontWeight: 600,
              boxShadow: '0 1px 3px rgba(0,0,0,0.3)'
            }}
          >
            {badgeContent()}
          </div>
        )}
      </div>
    </button>
  );
}
