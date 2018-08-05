
// * * * GENERATED VUE STORE MODULE * * *
import sync from "../sync.js";
const keyword="flow"
const state={
  flows: []
};

function Flow( data ){// base model

}
const getters={
  flows( state, getters, rootState, rootGetters ){
    return state.flows.map( flow=>{
      // let parent=flow.parent ? getters.flows.find( f=>f.id==flow.parent ) : undefined;
      // let children=getters.flows.filter( f=>f.parent==flow.id )
      return Object.assign({}, flow, {
        // parent, children
      });
    })
  }
};

const actions={
  CREATE_FLOW({ commit }, payload ){
    return sync.create( keyword, payload ).then( response=>{
      commit("ADD_FLOW", response.data );
      return response.data;
    })
  },
  DESTROY_FLOW({ commit }, id ){
    return sync.destroy( keyword, id ).then(()=>{
      commit("REMOVE_FLOW", id );
    })
  },
  UPDATE_FLOW({ commit }, payload ){
    return sync.update( keyword, payload ).then( response=>{
      commit("ADD_FLOW", response.data );
      return response.data;
    })
  }
}

const mutations={
  ADD_FLOW( state, payload ){
    let arr=( Array.isArray( payload ) ? payload : [ payload ]).slice();
    state.flows=state.flows.map( flow=>{
      let index=arr.findIndex( p=>p.id==flow.id );
      if( index >= 0 ){
        flow=arr[index];
        arr.splice( index, 1 );
      }
      return flow;
    });
    if( arr.length ) state.flows.push( ...arr );
  },
  REMOVE_FLOW( state, id ){
    state.flows=state.flows.filter( flow=>flow.id != id );
  }
};

export default{ state, getters, actions, mutations };
