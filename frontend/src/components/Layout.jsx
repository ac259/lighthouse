// Layout.jsx
import React from 'react';
import { motion } from 'framer-motion';

const Layout = ({ title, subtitle, children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } }}
      className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 to-black px-4 relative overflow-hidden"
    >
      {/* Background Lighting Effects */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 blur-3xl opacity-50"></div>
        <div className="absolute bottom-1/4 right-1/4 w-64 h-64 rounded-full bg-gradient-to-r from-pink-500 to-yellow-500 blur-3xl opacity-50"></div>
      </div>

      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.6, delay: 0.2 } }}
        className="text-6xl font-extrabold text-white mb-8 relative z-10"
      >
        {title || 'Lighthouse'}
      </motion.h1>

      {subtitle && (
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0, transition: { duration: 0.6, delay: 0.4 } }}
          className="text-lg text-gray-300 mb-12 relative z-10"
        >
          {subtitle}
        </motion.p>
      )}

      <div className="relative z-10 w-full flex justify-center">{children}</div>
    </motion.div>
  );
};

export default Layout;
