import React, { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import "./main.css"
import Layout from './Layout'
import { BrowserRouter } from 'react-router-dom'
import 'nprogress/nprogress.css';

const rootElement = document.getElementById('root');

if (rootElement) {
  const root = createRoot(rootElement);

  root.render(
    <StrictMode>
      <BrowserRouter>
        <Layout />
      </BrowserRouter>
    </StrictMode>
  );
} else {
  throw new Error('Root element not found');
}