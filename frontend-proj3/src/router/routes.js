
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: 'search-result/table', component: () => import('pages/SearchResult.vue') },
    ]
  },

  {
    path: '/search-result/',
    component: () => import('layouts/VisualizationLayout.vue'),
    children: [
      { path: 'graph', component: () => import('src/pages/RelationGraph.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes

