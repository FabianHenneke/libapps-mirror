/**
 * @fileoverview Rewrite ES6 import statements used by the GSC SSH agent
 * backend to immediately-invoked function expressions and create a bundle with
 * all node dependencies.
 */

import resolve from 'rollup-plugin-node-resolve';

export default {
  input: 'js/nassh_agent_backend_gsc.js',
  output: {
    file: 'js/nassh_agent_backend_gsc.concat.js',
    format: 'iife',
  },
  plugins: [
    resolve({
      jsnext: true
    })
  ],
};
