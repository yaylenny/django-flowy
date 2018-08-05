<script>
  import FlowItem from "../components/Flow.vue";
  import { mapGetters } from "vuex";
  let testItems=[
    { id: 1, index: 0, text: 'Item1', complete: false, parent: null },
    { id: 2, index: 1, text: 'Item 2', complete: false, parent: 1 },
    { id: 3, index: 0, text: 'Item 3', complete: true, parent: 1 },
    { id: 4, index: 1, text: 'Item 4', complete: false, parent: null },
    { id: 5, index: 0, text: 'Item 5', complete: false, parent: 4 },
  ];
  function findByProp( value, flows, prop="id" ){
    return flows.find( f=>f[prop]==value )
  }
  export default{
    props: {},
    data(){
      return {
        debug: true,
        items: [],
        active: 0,
        root: 0,
        ufid: 0,
        timer: 0,
        root: 0, // root flow visisble
        hovered: 0,
        retracted: [], //flows which are not expanded
      };
    },
    components:{
      FlowItem
    },
    computed:{
      ...mapGetters(['flows']),
      breadcrumbs(){
        if( this.root ){

        }
      },
      flowItems(){
        let items=(this.flows.length ? this.flows : testItems).slice();
        let roots=this.flows.filter( item=>!item.parent );
        roots.sort((a,b)=>a.index-b.index);
        return roots.map( item=>{
          return { ...item, children: this.buildChildren( item, items )}
        })
      }
    },
    methods:{
      log( text ){
        if( this.debug ){
          console.log( text );
        }
      },
      buildChildren( item, items ){
        return items.filter( i=>i.parent==item.id )
          .map( i=>{
            return { ...i, children: this.buildChildren( i, items )};
          })
      },
      activateItem( id ){
        this.$store.commit('ACTIVATE_ITEM', id );
      },
      createItem( data ){
        let item=Object.assign({
          index: 0,
          text: ' ',
          parent: null,
          complete: false
        }, data );
        if( item.id ) return console.error('Cannot create an item with an existing id, update instead');
        return this.$store.dispatch("CREATE_FLOW", item ).then( data=>{
          this.activateItem( data.id )
          return data;
        })
      },
      createSibling( id, data={} ){
        let item=this.findItem( id );
        if( item ){
          data=Object.assign({}, data, { parent: item.parent, index: item.index+1 });
          this.createItem( data );
        }
      },
      findChildren( id ){
        let item=this.findItem( id );
        if( item ){
          return this.flows.filter( f=>f.parent==id );
        }
        return [];
      },
      findItem( id ){
        if( !id ) return;
        id=id.id ? id.id : id;
        return findByProp( id, this.flows );
      },
      findSibling( id, prev=false ){
        let item=this.findItem( id );
        if( item ){
          let items=this.flows.filter( f=>{
            return f.parent==item.parent || !( f.parent || item.parent );
          });
          if( items.length < 2 ) return null;
          items.sort(( a, b )=>( a.index-b.index ));
          let index=items.findIndex( f=>f.id==id );
          index=prev ? index-1 : index+1;
          if( index >= 0 && index < items.length ){
            return items[ index ];
          }
          // if( prev ){
          //   if( index < 0 ) return null;
          //   return items[ index-1 ];
          // }
          // else{
          //   if( index >= items.length-1 ) return null;
          //   return items[ index+1 ]
          // }
        }
        return null;
      },
      indentItem( id ){
        let item=this.findItem( id );
        if( item ){
          let sibling=this.findSibling( id, true );
          if( sibling ){
            let children=this.findChildren( sibling.id );
            this.saveItem( id,{ parent: sibling.id, index: children.length })
          }
          else this.log('cannot indent without sibling')
        }
      },
      outdentItem( id ){
        let item=this.findItem( id );
        if( item && item.parent ){
          let parent=this.findItem( item.parent );
          if( parent ){
            this.saveItem( id,{ parent: parent.parent, index: parent.children.length })
          }
          else this.log('cannot outdent without parent')
        }
      },
      saveItem( id, data ){
        let item=this.findItem( id );
        if( !item ) return console.error('Cannot find item ', id );
        data=Object.assign({}, item, data, { id });
        return this.$store.dispatch("UPDATE_FLOW", data ).then( data=>{
          return data;
        })
      },
      onFocus( e, id ){
        console.log( 'focus', id )
        this.activateItem( id );
      },
      onBackout( e, id ){// user backspaced enough to delete
        let item=this.findItem( id );
        if( item ){

        }
      },
      onBlur( e, id ){
        console.log( 'blur', id )
      },
      onBullet( e, id ){
        console.log( 'onBullet')
      },
      onChange( id, text ){
        console.log( 'change', id, text )
        clearTimeout( this.timer );
        this.timer=setTimeout(()=>{
          clearTimeout( this.timer );
          if( text ){
            this.saveItem( id,{ text });
          }
        }, 500 );
      },
      onKeyDown( e, id ){
        console.log( 'keyDown', id )
      },
      onEnter( e, id ){
        console.log( 'enter', id )
        this.createSibling( id );
      },
      onMenu( e, id ){
        this.hovered=id;
      },
      onTab( e, id ){
        console.log( 'tab', id );
        this.indentItem( id );
      },
      onToggle( e, id ){
        let index=this.retracted.indexOf( id );
        if( index >= 0 ) this.retracted.splice( index, 1 );
        else this.retracted.push( id );
      }
    },
    created(){
      this.$store.dispatch('init');
    },
    watch:{}
  }
</script>
<template lang="pug">
  .vue-flow: .container: .flow-box
    .flow-toolbar
      .toolbar-left
        .toolbar-item: .flow-logo Vue Flowy
      .toolbar-right
        button.button.is-small.is-grey
          span Show completed
    .flow-breadcrumbs( v-if="root")
      .flow-breadcrumb( v-for="breadcrumb in breadcrumbs")
        a( @click="" ) {{breadcrumb.text}}
    .flow-items
      flow-item( v-for="(item,index) in flowItems"
        :text="item.text"
        :key="item.id"
        :id="item.id"
        :index="item.index"
        :parent="item.parent"
        :children="item.children"
        :expanded="(retracted.indexOf( item.id ) < 0)"
        :hovered="hovered==item.id"
        @toggle="onToggle"
        @menu="onMenu"
        @backout="onBackout"
        @change="onChange"
        @keydown="onKeyDown"
        @focus="onFocus"
        @blur="onBlur"
        @tab="onTab"
        @bullet="onBullet"
        @enter="onEnter")
</template>

<style lang="scss" src="../style.scss"></style>
