import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, useAnimation } from 'framer-motion';

const MotionLink = motion(Link);

const LandingPage = () => {
  const controls = useAnimation();

  useEffect(() => {
    controls.start({
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    });
  }, [controls]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={controls}
      className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 to-black px-4 relative overflow-hidden"
    >
      {/* Background Lighting Effect */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 blur-3xl opacity-50"></div>
        <div className="absolute bottom-1/4 right-1/4 w-64 h-64 rounded-full bg-gradient-to-r from-pink-500 to-yellow-500 blur-3xl opacity-50"></div>
      </div>

      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.6, delay: 0.2 } }}
        className="text-6xl font-extrabold text-white mb-8 relative z-10"
      >
        Lighthouse
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0, transition: { duration: 0.6, delay: 0.4 } }}
        className="text-lg text-gray-300 mb-12 relative z-10"
      >
        Illuminate your content with powerful analysis tools.
      </motion.p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
        <MotionLink
          to="/hate-speech-detection"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1, transition: { duration: 0.5, delay: 0.6 } }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex flex-col items-center p-8 bg-gray-800 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300"
        >
          <h2 className="text-2xl font-bold text-red-500 mb-4">Hate Speech Detection</h2>
          <p className="text-gray-400 text-center">
            Analyze text for hateful language and derogatory expressions.
          </p>
        </MotionLink>

        <MotionLink
          to="/fake-news-detection"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1, transition: { duration: 0.5, delay: 0.8 } }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex flex-col items-center p-8 bg-gray-800 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300"
        >
          <h2 className="text-2xl font-bold text-blue-500 mb-4">Fake News Detection</h2>
          <p className="text-gray-400 text-center">
            Examine content for misinformation and verify claims.
          </p>
        </MotionLink>
      </div>
    </motion.div>
  );
};

export default LandingPage;
