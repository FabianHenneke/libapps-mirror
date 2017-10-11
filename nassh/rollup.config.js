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
