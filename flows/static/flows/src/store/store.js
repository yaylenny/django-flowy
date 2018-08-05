// IMPORT MODULES
import flow from "./modules/flow.js";
import sync from "./sync.js";

const state={
  active: 0, // id of active flow item
  user:{
    name: '',
    id: 0
  }
};
const modules={
  flow
};

const getters={
  username:state=>state.user.name,
  userid:state=>state.user.id
};

const actions={
  init({ commit }){
    return sync.init().then( response=>{
      let { user, flows }=response.data;
      commit("SET_USER", user );
      commit("ADD_FLOW", flows );
      return response;
    });
  }
}

const mutations={
  ACTIVATE_ITEM( state, item ){
    if( item ){
      state.active=item.id || item;
    }
  },
  SET_USER( state, user ){
    state.user=user;
  }
};

export default{ state, modules, getters, actions, mutations };
